import logging
from datetime import datetime, timedelta

from celery_scheduler.app.celery_app import celery_app
from db_controllers import get_current_controller_class
from telegram_service import TelegramService
from config import Config
from fields import MessageExtractedFields

db_controller = get_current_controller_class(Config.DB_CONTROLLER)
db_controller = db_controller()

tl_service = TelegramService()


@celery_app.task
def check_publications():
    # Get the latest 10 messages from the channel
    latest_msg = db_controller.get_last_added_message()
    logging.info(f"Last message id {latest_msg[MessageExtractedFields.MESSAGE_ID]}")
    msg_bodies = tl_service.get_messages(min_message_id=latest_msg[MessageExtractedFields.MESSAGE_ID])
    logging.info(f"Received message IDs {list(msg_bodies.keys())}")
    msg_to_insert = list(msg_bodies.values())
    if msg_to_insert:
        db_controller.insert_bulk_messages(msg_to_insert)
    logging.info(f"Added {len(msg_bodies)} messages to the {type(db_controller).__name__}")
    return {"count": len(msg_bodies)}


@celery_app.task
def remove_old_publications():
    # Remove records that were added more than 1 month ago
    one_month_ago = datetime.now() - timedelta(days=30)
    deleted_records = db_controller.delete_old_messages(one_month_ago)
    return {"count": deleted_records}
