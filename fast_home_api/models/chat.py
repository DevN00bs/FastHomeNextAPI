from marshmallow import Schema
from marshmallow.fields import String, Integer, Function
from marshmallow_enum import EnumField as Enum
from mongoengine import EmbeddedDocument
from mongoengine.fields import StringField, EnumField, IntField

from ..utils.enums import ChatEventType


class ChatEvent(EmbeddedDocument):
    event_type = EnumField(ChatEventType, required=True)
    content = StringField(required=True)
    description = StringField()
    date = IntField(required=True)
    from_id = StringField(required=True)
    property_id = StringField(required=True)


class ChatEnterRequest(Schema):
    token = String(required=True)


class ChatMessageRequest(Schema):
    token = String(required=True)
    message = String(required=True)
    to_user_id = String(required=True)
    date = Integer()
    property_id = String(required=True)


class ChatEventResponse(Schema):
    event_type = Enum(ChatEventType)
    content = String()
    description = String()
    date = Integer()
    from_id = String()
    property_id = String()


class StartConversationRequest(Schema):
    property_id = String(required=True)
    token = String(required=True)
    issuer_id = String()


class StartConversationResponse(Schema):
    thumbnail_id = Function(
        lambda prop: str(prop.photo_list.first().photo.thumbnail._id) if prop.photo_list.first() is not None else None)
    address = String()
    user_id = Function(lambda prop: str(prop.owner.id))
    username = Function(lambda prop: prop.owner.username)


class IssuerDataResponse(Schema):
    username = String()
