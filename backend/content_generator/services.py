import hashlib
import json
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import timedelta

from django.conf import settings
from django.utils import timezone


@dataclass(frozen=True)
class ContentResult:
    caption: str
    hashtags: list[str]
    title: str
    description: str
    suggested_publish_time: str
    provider: str
    metadata: dict

    def to_dict(self):
        return asdict(self)


def _keywords(idea: str, language: str) -> list[str]:
    words = re.findall(r'[\w\u0600-\u06ff]+', idea.lower(), flags=re.UNICODE)
    stop = {'the', 'and', 'for', 'with', 'this', 'that', 'یک', 'برای', 'با', 'از', 'به', 'در'}
    unique = []
    for word in words:
        if len(word) > 2 and word not in stop and word not in unique:
            unique.append(word)
    fallback = ['content', 'creator'] if language == 'en' else ['محتوا', 'تولیدمحتوا']
    return (unique or fallback)[:6]


def _next_slot(seed: int):
    now = timezone.now()
    hour = (9, 12, 18, 20)[seed % 4]
    candidate = (now + timedelta(days=1)).replace(hour=hour, minute=0, second=0, microsecond=0)
    return candidate.isoformat()


def generate_local(*, idea: str, platform: str, language: str, tone: str) -> ContentResult:
    normalized = ' '.join(idea.split()).strip()
    digest = hashlib.sha256(f'{platform}|{language}|{tone}|{normalized}'.encode()).hexdigest()
    seed = int(digest[:8], 16)
    keys = _keywords(normalized, language)
    hashtags = [f"#{re.sub(r'[^\w\u0600-\u06ff]', '', item)}" for item in keys]

    if language == 'fa':
        intros = ('یک نگاه تازه:', 'ایده امروز:', 'بیایید کاربردی نگاه کنیم:')
        caption = f'{intros[seed % len(intros)]} {normalized}\n\nنظر شما چیست؟'
        title = f'{normalized[:70]}؛ راهنمای کاربردی'
        description = f'در این محتوا درباره «{normalized}» صحبت می‌کنیم و نکات قابل اجرا را مرور می‌کنیم.'
    else:
        intros = ('A fresh perspective:', 'Today’s practical idea:', 'Let’s make this actionable:')
        caption = f'{intros[seed % len(intros)]} {normalized}\n\nWhat would you add?'
        title = f'{normalized[:70]}: A practical guide'
        description = f'Explore {normalized} with clear, actionable takeaways for creators and their audiences.'

    if platform == 'twitter':
        caption = caption.replace('\n\n', ' ')[:260]
        title = ''
        description = ''
        hashtags = hashtags[:3]
    elif platform == 'youtube':
        caption = description
        hashtags = hashtags[:8]
    else:
        title = ''
        description = ''
        hashtags = hashtags[:12]

    return ContentResult(
        caption=caption,
        hashtags=hashtags,
        title=title,
        description=description,
        suggested_publish_time=_next_slot(seed),
        provider='local',
        metadata={'deterministic': True, 'tone': tone},
    )


def _external_prompt(*, idea: str, platform: str, language: str, tone: str) -> str:
    return (
        'Return only a JSON object with caption, hashtags (array), title, description. '
        f'Create {language} content for {platform} in a {tone} tone. Idea: {idea}. '
        'For Instagram prioritize caption and hashtags; for Twitter keep caption under 280 characters; '
        'for YouTube provide an SEO title and detailed description.'
    )


def generate_openai_compatible(*, idea: str, platform: str, language: str, tone: str) -> ContentResult:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY is not configured')
    payload = json.dumps({
        'model': settings.CONTENT_GENERATION_MODEL,
        'response_format': {'type': 'json_object'},
        'messages': [{'role': 'user', 'content': _external_prompt(
            idea=idea, platform=platform, language=language, tone=tone
        )}],
        'temperature': 0.7,
    }).encode()
    request = urllib.request.Request(
        f"{settings.CONTENT_GENERATION_BASE_URL.rstrip('/')}/chat/completions",
        data=payload,
        headers={'Authorization': f'Bearer {settings.OPENAI_API_KEY}', 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=settings.CONTENT_GENERATION_TIMEOUT) as response:
            raw = json.loads(response.read().decode())
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError(f'content provider request failed: {exc}') from exc
    data = json.loads(raw['choices'][0]['message']['content'])
    local = generate_local(idea=idea, platform=platform, language=language, tone=tone)
    return ContentResult(
        caption=str(data.get('caption') or local.caption),
        hashtags=[str(item) for item in data.get('hashtags', local.hashtags)],
        title=str(data.get('title') or local.title),
        description=str(data.get('description') or local.description),
        suggested_publish_time=local.suggested_publish_time,
        provider='openai',
        metadata={'model': settings.CONTENT_GENERATION_MODEL},
    )


def generate_content(*, idea: str, platform: str, language: str = 'en', tone: str = 'professional') -> ContentResult:
    provider = settings.CONTENT_GENERATION_PROVIDER
    if provider in {'openai', 'openai-compatible'}:
        try:
            return generate_openai_compatible(idea=idea, platform=platform, language=language, tone=tone)
        except RuntimeError as exc:
            fallback = generate_local(idea=idea, platform=platform, language=language, tone=tone)
            return ContentResult(**{**fallback.to_dict(), 'metadata': {
                **fallback.metadata, 'fallback_from': provider, 'fallback_reason': str(exc)[:200]
            }})
    return generate_local(idea=idea, platform=platform, language=language, tone=tone)
