from typing import Literal

from bson.objectid import ObjectId
from marshmallow import ValidationError

token_audiences: type = Literal["verify", "forgot"]
contract_types: type = Literal["sale", "rent"]

allowed_mimetypes = [
    "image/jpeg",
    "image/png",
    "image/webp"
]


def is_valid_id(value):
    if not ObjectId.is_valid(value):
        raise ValidationError("Not a valid ID")
