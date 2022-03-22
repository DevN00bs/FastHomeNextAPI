from marshmallow import Schema
from marshmallow.fields import String, Integer
from mongoengine import EmbeddedDocument
from mongoengine.fields import StringField, EnumField, IntField
from marshmallow_enum import EnumField as Enum

from ..utils.enums import ChatEventType


class ChatEvent(EmbeddedDocument):
    event_type = EnumField(ChatEventType, required=True)
    content = StringField(required=True)
    description = StringField()
    date = IntField(required=True)
    from_id = StringField(required=True)


class ChatEnterRequest(Schema):
    token = String(required=True)


class ChatMessageRequest(Schema):
    token = String(required=True)
    message = String(required=True)
    to_user_id = String(required=True)
    date = Integer()


class ChatEventResponse(Schema):
    event_type = Enum(ChatEventType)
    content = String()
    description = String()
    date = Integer()
