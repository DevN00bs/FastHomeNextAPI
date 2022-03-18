from marshmallow import Schema
from marshmallow.fields import String


class ChatEnterRequest(Schema):
    token = String(required=True)
