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
