from celery import Celery

CELERY_BROKER_URL = ''
CELERY_RESULT_BACKEND = ''

celery_app = Celery('app', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)