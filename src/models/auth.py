from typing import get_args

from apiflask.fields import String, Email
from apiflask.schemas import Schema
from apiflask.validators import Length, OneOf
from mongoengine import Document, StringField, EmailField, BooleanField

from ..utils.types import token_audiences


# TODO: model - controller - routes
# Borrar (?)
# Para separar endpoint de controller trabajar embeddeddocs
class User(Document):
    username = StringField(unique=True)
    email = EmailField(unique=True)
    passwd_hash = StringField()
    is_verified = BooleanField(default=True)
    last_token = StringField()
    phone = StringField()
    contact_email = StringField()
    fb_link = StringField()
    insta_link = StringField()
    twit_link = StringField()
    meta = {"collection": "users"}


class RegistrationRequest(Schema):
    username = String(required=True)
    password = String(required=True, validate=Length(5))
    email = Email(required=True)


class LoginRequest(Schema):
    username = String(required=True)
    password = String(required=True)


class LoginResponse(Schema):
    token = String()


class SendEmailRequest(Schema):
    purpose = String(required=True, validate=OneOf(get_args(token_audiences)))
    email = Email(required=True)


class ForgotPasswordRequest(Schema):
    token = String(required=True)
    new_password = String(required=True, validate=Length(5))


class PropertyOwnerInfo(Schema):
    username = String()
