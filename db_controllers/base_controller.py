import datetime
from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def __init__(self):
        """
        Constructor method for BaseController.

        This method should be overridden by subclasses to provide their own
        initialization logic.
        """
        pass

    @abstractmethod
    def get_all_messages(self, channel_id=None) -> list:
        """
        Get all messages from the channel.

        Parameters:
            channel_id (optional): The ID of the channel to retrieve messages from.

        Returns:
            A list of dictionaries representing the messages in the channel.
        """
        pass

    @abstractmethod
    def get_last_added_message(self, channel_id=None) -> dict:
        """
        Get the last added message from the channel.

        Returns:
            A dictionary representing the last added message in the channel.
        """
        pass

    @abstractmethod
    def get_filtered_messages(self) -> list:
        """
        Get filtered messages from the channel.

        Returns:
            A list of dictionaries representing the filtered messages in the channel.
        """
        pass

    @abstractmethod
    def insert_new_message(self, msg: dict) -> int:
        """
        Insert a new message into the database.

        Parameters:
            msg: A dictionary representing the message to insert.
        """
        pass

    @abstractmethod
    def insert_bulk_messages(self, messages: list) -> list:
        """
        Insert multiple messages into the database.

        Parameters:
            messages: A list of dictionaries representing the messages to insert.
        """
        pass

    @abstractmethod
    def delete_message(self, msg_id: int) -> int:
        """
        Delete a message from the database.

        Parameters:
            msg_id: The ID of the message to delete.
        """
        pass

    @abstractmethod
    def delete_bulk_messages(self, message_ids: list) -> int:
        """
        Delete multiple messages from the database.

        Parameters:
            message_ids: A list of message IDs to delete.
        """
        pass

    def delete_old_messages(self, old_date: datetime.datetime) -> int:
        """
        Delete multiple messages, which date is older than the given

        Parameters:
            old_date: datetime
        """
        pass
