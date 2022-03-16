import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Email


class ProfileDoc(m.EmbeddedDocument):
    phone_number = m.StringField(default="")
    contact_email = m.EmailField()
    facebook_link = m.StringField(default="")
    instagram_link = m.StringField(default="")
    twitter_link = m.StringField(default="")


class ProfileData(Schema):
    phone_number = String()
    contact_email = Email()
    facebook_link = String()
    instagram_link = String()
    twitter_link = String()
