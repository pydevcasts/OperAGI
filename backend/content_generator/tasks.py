import logging
from functools import wraps

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import AnalyticsSnapshot, GeneratedContent, Post, Schedule
from .services import generate_content

logger = logging.getLogger(__name__)

try:
    from celery import shared_task
except ImportError:
    def shared_task(*decorator_args, **decorator_kwargs):
        def decorator(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                return func(*args, **kwargs)
            wrapped.delay = wrapped
            wrapped.apply_async = lambda args=None, kwargs=None, **options: wrapped(*(args or ()), **(kwargs or {}))
            return wrapped
        return decorator


@shared_task(name='content_generator.tasks.generate_post_content')
def generate_post_content(post_id):
    post = Post.objects.get(pk=post_id)
    post.status = Post.Status.GENERATING
    post.generation_error = ''
    post.save(update_fields=('status', 'generation_error', 'updated_at'))
    try:
        result = generate_content(
            idea=post.content, platform=post.platform, language=post.language, tone=post.tone
        )
        with transaction.atomic():
            generated, _ = GeneratedContent.objects.update_or_create(
                post=post,
                defaults={
                    'generated_text': result.caption,
                    'title': result.title,
                    'description': result.description,
                    'suggested_hashtags': ' '.join(result.hashtags),
                    'hashtags': result.hashtags,
                    'suggested_publish_time': result.suggested_publish_time,
                    'provider': result.provider,
                    'provider_metadata': result.metadata,
                },
            )
            post.status = Post.Status.GENERATED
            post.save(update_fields=('status', 'updated_at'))
        return generated.pk
    except Exception as exc:
        logger.exception('Content generation failed for post %s', post_id)
        post.status = Post.Status.FAILED
        post.generation_error = str(exc)[:1000]
        post.save(update_fields=('status', 'generation_error', 'updated_at'))
        raise


@shared_task(name='content_generator.tasks.publish_scheduled_post')
def publish_scheduled_post(schedule_id):
    schedule = Schedule.objects.select_related('post').get(pk=schedule_id)
    if schedule.status != Schedule.Status.QUEUED:
        return schedule.status
    if not schedule.is_due:
        return 'not_due'
    schedule.status = Schedule.Status.PROCESSING
    schedule.save(update_fields=('status', 'updated_at'))
    try:
        if settings.SOCIAL_PUBLISH_MODE != 'simulate':
            raise RuntimeError('Live social publishing is not configured; use simulate mode or configure a provider adapter.')
        now = timezone.now()
        post = schedule.post
        post.status = Post.Status.PUBLISHED
        post.published_at = now
        post.save(update_fields=('status', 'published_at', 'updated_at'))
        schedule.status = Schedule.Status.PUBLISHED
        schedule.processed_at = now
        schedule.last_error = ''
        schedule.save(update_fields=('status', 'processed_at', 'last_error', 'updated_at'))
        AnalyticsSnapshot.objects.get_or_create(
            user=post.user, post=post, platform=post.platform, captured_at=now,
            defaults={'social_account': post.social_account, 'metadata': {'source': 'local-publish-simulation'}},
        )
        return schedule.status
    except Exception as exc:
        schedule.status = Schedule.Status.FAILED
        schedule.last_error = str(exc)[:1000]
        schedule.save(update_fields=('status', 'last_error', 'updated_at'))
        raise


@shared_task(name='content_generator.tasks.process_due_schedules')
def process_due_schedules():
    due_ids = list(Schedule.objects.filter(
        status=Schedule.Status.QUEUED, scheduled_for__lte=timezone.now()
    ).values_list('id', flat=True)[:100])
    for schedule_id in due_ids:
        publish_scheduled_post(schedule_id)
    return len(due_ids)


def enqueue(task, *args, eta=None):
    """Queue a task when possible; otherwise execute only immediately-due work."""
    if hasattr(task, 'apply_async'):
        try:
            result = task.apply_async(args=args, eta=eta)
            return getattr(result, 'id', '') or '', bool(settings.CELERY_TASK_ALWAYS_EAGER)
        except Exception as exc:
            logger.warning('Celery unavailable, using safe fallback: %s', exc)
    if eta is None or eta <= timezone.now():
        task(*args)
        return 'sync', True
    return 'local-pending', True
