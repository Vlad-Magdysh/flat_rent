from celery_scheduler.app.celery import celery_app

@celery_app.task
def check_publications():
    # Get the latest 10 messages from the channel
    pass

@celery_app.task
def remove_old_publications():
    # Remove records that were added more than 1 month ago
    pass
