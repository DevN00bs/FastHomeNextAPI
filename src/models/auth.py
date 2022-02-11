from apiflask.fields import String, Email
from apiflask.schemas import Schema
from apiflask.validators import Length
from mongoengine import Document, StringField, EmailField, BooleanField


class User(Document):
    username = StringField(unique=True)
    email = EmailField(unique=True)
    passwd_hash = StringField()
    is_verified = BooleanField(default=False)
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
