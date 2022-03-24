import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Email, Float, Integer, Nested, Function


class PropsInfo(Schema):
    address = String()
    description = String()
    price = Float()
    terrain_height = Float()
    terrain_width = Float()
    bedrooms_amount = Integer()
    bathrooms_amount = Float()
    floors_amount = Integer()
    garage_size = Integer()
    contract_type = String()
    currency_code = String()
    thumbnail_id = Function(
        lambda prop: str(prop.photo_list.first().photo.thumbnail._id) if prop.photo_list.first() is not None else None)


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
    properties_list = Nested(PropsInfo, data_key="pub_props", many=True)
