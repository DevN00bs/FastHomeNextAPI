from apiflask.fields import String, Email
from apiflask.schemas import Schema
from apiflask.validators import Length
from mongoengine import Document, StringField, EmailField, BooleanField


class User(Document):
    username = StringField()
    email = EmailField()
    passwd_hash = StringField()
    is_verified = BooleanField(default=False)
    last_token = StringField()
    phone = StringField()
    contact_email = StringField()
    fb_link = StringField()
    insta_link = StringField()
    twit_link = StringField()


class RegistrationRequest(Schema):
    username = String(required=True)
    password = String(required=True, validate=Length(5))
    email = Email(required=True)
