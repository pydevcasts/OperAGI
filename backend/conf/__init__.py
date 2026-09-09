try:
    from .celery import app as celery_app
except ImportError:  # Celery remains optional for lightweight local setup.
    celery_app = None

__all__ = ('celery_app',)
