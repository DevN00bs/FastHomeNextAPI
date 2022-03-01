import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Email


class ProfileDoc(m.EmbeddedDocument):
    phone = m.StringField(default="")
    contact_email = m.EmailField(default="")
    fb_link = m.StringField(default="")
    insta_link = m.StringField(default="")
    twit_link = m.StringField(default="")


class ProfileData(Schema):
    phone = String()
    contact_email = Email()
    fb_link = String()
    insta_link = String()
    twit_link = String()
