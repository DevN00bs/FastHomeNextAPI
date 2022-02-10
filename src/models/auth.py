from apiflask.fields import String, Email
from apiflask.schemas import Schema
from apiflask.validators import Length
from mongoengine import Document, StringField, EmailField, BooleanField


class User(Document):
    username = StringField()
    email = EmailField()
    passwdHash = StringField()
    isVerified = BooleanField()
    lastToken = StringField()
    phone = StringField()
    contactEmail = StringField()
    fbLink = StringField()
    instaLink = StringField()
    twitLink = StringField()


class RegistrationRequest(Schema):
    username = String(required=True)
    password = String(required=True, validate=Length(5))
    email = Email(required=True)
