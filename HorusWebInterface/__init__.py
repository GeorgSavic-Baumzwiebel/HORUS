# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import celery
celery_app = celery.app
__all__ = ('celery_app',)

from celery.contrib.pytest import celery_app