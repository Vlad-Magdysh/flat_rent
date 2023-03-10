from datetime import timedelta
from celery_scheduler.app import tasks
from celery_scheduler.app.celery import celery_app

_ = tasks

if __name__ == '__main__':
    # Schedule tasks to run every 5 minutes and every day respectively
    celery_app.conf.beat_schedule = {
        'check-publications': {
            'task': 'tasks.check_publications',
            'schedule': timedelta(minutes=5)
        },
        'remove-old-publications': {
            'task': 'tasks.remove_old_publications',
            'schedule': timedelta(days=1)
        }
    }
    celery_app.conf.timezone = 'UTC'
    celery_app.worker_main(['-A', 'app', '--loglevel=INFO', '--concurrency=1', '--beat'])