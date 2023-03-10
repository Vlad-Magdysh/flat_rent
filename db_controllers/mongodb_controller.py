from pymongo import MongoClient

from db_controllers.base_controller import BaseController
from fields import MessageExtractedFields

# TODO Don`t use config directly. Provide another solution
from config import Config


class MongoController(BaseController):
    def __init__(self):
        super().__init__()
        self.client = MongoClient(Config.MONGO_URI)
        self.flat_db = self.client.flat_rent
        self.messages_collection = self.flat_db.messages

    def get_all_messages(self, channel_id=None) -> list:
        if channel_id is not None:
            messages = self.messages_collection.find(
                {MessageExtractedFields.CHANNEL_ID: channel_id}
            )
        else:
            messages = self.messages_collection.find()
        return list(messages)

    def get_last_added_message(self, channel_id=None) -> list:
        return self.messages_collection.find_one(sort=[(MessageExtractedFields.P_DATE, -1)])

    # TODO implement this function. Think what parameters should be used.
    def get_filtered_messages(self):
        pass

    def insert_new_message(self, msg: dict):
        self.messages_collection.insert_one(msg)

    def insert_bulk_messages(self, messages: list):
        self.messages_collection.insert_many(messages)

    def delete_message(self, msg_id):
        self.messages_collection.delete_one({MessageExtractedFields.MESSAGE_ID: msg_id})

    def delete_bulk_messages(self, message_ids: list):
        self.messages_collection.delete_many(
            {
                MessageExtractedFields.MESSAGE_ID: {"$in": message_ids}
            }
        )
