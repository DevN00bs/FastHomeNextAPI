from email.policy import default
import mongoengine as m
from apiflask import Schema
from apiflask.fields import String


class ProfileDoc(m.EmbeddedDocument):
    phone = m.StringField(default="")
    contact_email = m.StringField(default="")
    fb_link = m.StringField(default="")
    insta_link = m.StringField(default="")
    twit_link = m.StringField(default="")


class ProfileData(Schema):
    phone = String()
    contact_email = String()
    fb_link = String()
    insta_link = String()
    twit_link = String()
