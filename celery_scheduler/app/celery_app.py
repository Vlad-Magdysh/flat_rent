from celery import Celery

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#CELERY_RESULT_BACKEND = ''

celery_app = Celery('celery_app', broker=CELERY_BROKER_URL)
