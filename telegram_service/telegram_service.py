import logging
import os
from collections import defaultdict
from typing import Optional

import telethon.tl.custom
from telethon.sync import TelegramClient

from config import Config
from fields import MessageExtractedFields
from utils import get_cleared_dict

logging.getLogger('telethon').setLevel(logging.WARNING)


class TelegramService:
    """
    Class that provide an interface to Telegram API
    """

    def __init__(self, parser=None, session_path=None):
        if session_path is not None:
            self.session_path = session_path
        else:
            self.session_path = Config.SESSION_PATH

        self.parser = parser
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
        # TODO make group_name a parameter. Parser will be chosen by GROUP_NAME
        entity = self.telegram_client.get_entity(Config.GROUP_NAME)
        messages = self.telegram_client.get_messages(entity, limit=limit, min_id=min_message_id)

        grouped_photos = defaultdict(list)
        grouped_ids = defaultdict(list)
        transformed_messages = dict()

        for msg in messages:
            photo_path = self.download_photo(msg)
            if photo_path is not None:
                grouped_photos[msg.grouped_id].append(photo_path)
                grouped_ids[msg.grouped_id].append(msg.id)

            # TODO Store mapping of parsers for the channels
            if not msg.message:
                continue
            elif self.parser is not None:
                flat_properties = self.parser.parse(msg.message)
                transformed_messages[msg.id] = get_cleared_dict(flat_properties)
            else:
                transformed_messages[msg.id] = {}

            if entity.username:
                link = f"https://t.me/{entity.username}/{msg.id}"
            else:
                link = f"https://t.me/c/{str(entity.id)[4:]}/{msg.id}"

            # NOTE1 grouped_ids[message.grouped_id] always contains at least 1 value
            # NOTE2 grouped_photos[message.grouped_id] will be extended and associated with transformed_messages.
            transformed_messages[msg.id].update({
                MessageExtractedFields.MESSAGE_ID: msg.id,
                MessageExtractedFields.TEXT: msg.message,
                MessageExtractedFields.LINK: link,
                MessageExtractedFields.P_DATE: msg.date,
                MessageExtractedFields.CHANNEL_ID: msg.peer_id.channel_id,
                MessageExtractedFields.GROUPED_ID: msg.grouped_id,
                MessageExtractedFields.ALL_IDS: grouped_ids[msg.grouped_id],
                MessageExtractedFields.LIST_PHOTO_PATHS: grouped_photos[msg.grouped_id]
            })
        for msg_properties in transformed_messages.values():
            msg_properties[MessageExtractedFields.MAX_ID]: max(MessageExtractedFields.ALL_IDS)

        return transformed_messages

    @staticmethod
    def download_photo(message: telethon.tl.custom.Message):
        """
        Downloads a photo.
        Path format: PHOTOS_ROOT/MESSAGE_GROUP_ID/PHOTO_ID.png
        :param message:
        :return: path to the saved photo
        """
        if message.photo is None:
            return None

        photo_dir = os.path.join(Config.PHOTOS_ROOT, str(message.grouped_id))
        if not os.path.isdir(photo_dir):
            os.mkdir(photo_dir)

        file_path = os.path.join(photo_dir, str(message.photo.id))
        if os.path.isfile(file_path):
            logging.warning(f"File {file_path} already exists. Skip downloading")
        return message.download_media(file_path)

    def get_last_message_id(self):
        entity = self.telegram_client.get_entity(Config.GROUP_NAME)
        messages = self.telegram_client.get_messages(entity, limit=1)
        return messages[0].id
