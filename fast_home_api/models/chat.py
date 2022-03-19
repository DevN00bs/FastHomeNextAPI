from marshmallow import Schema
from marshmallow.fields import String, Integer
from datetime import datetime


class ChatEnterRequest(Schema):
    token = String(required=True)


class ChatMessageRequest(Schema):
    token = String(required=True)
    message = String(required=True)
    to_user_id = String(required=True)
    date = Integer(load_default=int(datetime.now().timestamp()))

