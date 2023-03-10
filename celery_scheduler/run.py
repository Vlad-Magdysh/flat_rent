from datetime import timedelta
from celery_scheduler.app import tasks
from celery_scheduler.app.celery_app import celery_app

_ = tasks

if __name__ == '__main__':
    # Schedule tasks to run every 5 minutes and every day respectively
    celery_app.conf.beat_schedule = {
        'check-publications': {
            'task': 'celery_scheduler.app.tasks.check_publications',
            'schedule': timedelta(minutes=1)
        },
        'remove-old-publications': {
            'task': 'celery_scheduler.app.tasks.remove_old_publications',
            'schedule': timedelta(days=1)
        }
    }
    celery_app.conf.timezone = 'UTC'
    celery_app.start(["worker", '--loglevel=INFO', '--concurrency=1', '--beat'])