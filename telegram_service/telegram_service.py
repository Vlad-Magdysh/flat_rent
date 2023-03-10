import os
from collections import defaultdict

import telethon.tl.custom
from telethon.sync import TelegramClient

from config import Config
from fields import MessageExtractedFields


class TelegramService:
    """
    Class that provide an interface to Telegram API
    """

    def __init__(self, session_path=None):
        if session_path is not None:
            self.session_path = session_path
        else:
            self.session_path = Config.SESSION_PATH

        self.channel_name = Config.GROUP_NAME
        self.telegram_client = TelegramClient(self.session_path, Config.API_ID, Config.API_HASH)
        self.telegram_client.start()

    def get_messages(self, limit=None, min_message_id=0) -> dict:
        """
        Pull messages from the channel and extract necessary information.
        Group all photos into a message and parse and transform some fields

        :param limit: int,
        :param min_message_id: int
        :return: dict[message_id] = dict
        """
        entity = self.telegram_client.get_entity(Config.GROUP_NAME)
        messages = self.telegram_client.get_messages(entity, limit=limit, min_id=min_message_id)

        grouped_photos = defaultdict(list)
        grouped_ids = defaultdict(list)
        transformed_messages = dict()

        for msg in messages:
            photo_path = self.download_photo(msg)
            grouped_photos[msg.grouped_id].append(photo_path)
            grouped_ids[msg.grouped_id].append(msg.id)
            # TODO make parser for the given information. Extract flat price, size, address and so on
            # TODO Store mapping of parsers for the channels
            if not msg.message:
                continue

            if entity.username:
                link = f"https://t.me/{entity.username}/{msg.id}"
            else:
                link = f"https://t.me/c/{str(entity.id)[4:]}/{msg.id}"

            # NOTE1 grouped_ids[message.grouped_id] always contains at least 1 value
            # NOTE2 grouped_photos[message.grouped_id] will be extended and associated with transformed_messages.
            transformed_messages[msg.id] = {
                MessageExtractedFields.MESSAGE_ID: msg.id,
                MessageExtractedFields.TEXT: msg.message,
                MessageExtractedFields.LINK: link,
                MessageExtractedFields.P_DATE: msg.date,
                MessageExtractedFields.CHANNEL_ID: msg.peer_id.channel_id,
                MessageExtractedFields.GROUPED_ID: msg.grouped_id,
                MessageExtractedFields.ALL_IDS: grouped_ids[msg.grouped_id],
                MessageExtractedFields.MAX_ID: max(grouped_ids[msg.grouped_id]),
                MessageExtractedFields.LIST_PHOTO_PATHS: grouped_photos[msg.grouped_id]
            }

        return transformed_messages

    @staticmethod
    def download_photo(message: telethon.tl.custom.Message):
        """
        Downloads a photo.
        Path format: PHOTOS_ROOT/MESSAGE_GROUP_ID/PHOTO_ID.png
        :param message:
        :return: path to the saved photo
        """
        photo_dir = os.path.join(Config.PHOTOS_ROOT, str(message.grouped_id))
        if not os.path.isdir(photo_dir):
            os.mkdir(photo_dir)

        file_path = os.path.join(photo_dir, str(message.media.photo.id))
        return message.download_media(file_path)

    def get_last_message_id(self):
        entity = self.telegram_client.get_entity(Config.GROUP_NAME)
        messages = self.telegram_client.get_messages(entity, limit=1)
        return messages[0].id
