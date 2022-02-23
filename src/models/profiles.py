from mongoengine import Document, StringField, EmailField
from apiflask import Schema
from apiflask.fields import String


# Left some fields in case to use them later


class ProfileDoc(Document):
    username = StringField(unique=True)
    email = EmailField(unique=True)
    phone = StringField()
    contact_email = StringField()
    fb_link = StringField()
    insta_link = StringField()
    twit_link = StringField()
    # prop_list
    meta = {"collection": "profiles"}


class ProfileConfig(Schema):
    id = String()
    username = String()
    email = String()
    phone = String()
    contact_email = String()
    fb_link = String()
    insta_link = String()
    twit_link = String()
    # Prop_list


class ProfileRead(Schema):
    email = String()
    phone = String()
    contact_email = String()
    fb_link = String()
    insta_link = String()
    twit_link = String()
    # Prop_list


class ProfileUpdate(Schema):
    id = String(required=True)
    username = String()
    email = String()
    phone = String()
    contact_email = String()
    fb_link = String()
    insta_link = String()
    twit_link = String()
    # Prop_list

# TODO: Delete account (?)


class ProfileDelete(Schema):
    id = String(required=True)
