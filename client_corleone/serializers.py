"""Converts the JSON received from the bot to fancy Python objects."""
from abc import abstractmethod

from client_corleone.models import Chat, Message, Update


class Serializer:
    """Converts the JSON received from the bot to fancy Python objects."""

    @property
    def data(self):
        """Magic happens here. It returns your fresh objects (or a list of them)."""
        result = [self.serialize(datum) for datum in self._raw_data]
        return result if self.many else result[0]

    @abstractmethod
    def serialize(self, raw_data):
        """Provide here the way to go from json (as a dict) to python classes."""

    def __init__(self, raw_data, many=False):
        """Instantiate a serializer.

        * raw_data: The data received from the bot
        * many: Means that the data is a list of things
        """
        self.many = many
        self._raw_data = raw_data if many else [raw_data]


class UpdateSerializer(Serializer):
    """Converts the JSON received from the bot to fancy Python update objects."""

    def serialize(self, raw_data):
        """Serialize updates, while serializing their contained messages."""
        message = MessageSerializer(raw_data['message']).data
        return Update(raw_data['update_id'], message)


class MessageSerializer(Serializer):
    """Converts the JSON received from the bot to fancy Python message objects."""

    def serialize(self, raw_data):
        """Serialize messages, while serializing their contained chat_info."""
        chat = ChatSerializer(raw_data['chat']).data
        return Message(
            raw_data['message_id'], raw_data['from'],
            chat, raw_data['date'], raw_data['text']
        )


class ChatSerializer(Serializer):
    """Converts the JSON received from the bot to fancy Python chat objects."""

    def serialize(self, raw_data):
        """Serialize chat_info within messages."""
        return Chat(cid=raw_data['id'], first_name=raw_data['first_name'], ctype=raw_data['type'])
