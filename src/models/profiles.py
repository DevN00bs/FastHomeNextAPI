import mongoengine as m
from apiflask import Schema
from apiflask.fields import String

from ..models.auth import User


class ProfileDoc(m.Document):
    user = m.ReferenceField(User, reverse_delete_rule=m.CASCADE)
    phone = m.StringField()
    contact_email = m.StringField()
    fb_link = m.StringField()
    insta_link = m.StringField()
    twit_link = m.StringField()
    meta = {"collection": "profiles"}


class ProfileData(Schema):
    phone = String()
    contact_email = String()
    fb_link = String()
    insta_link = String()
    twit_link = String()
