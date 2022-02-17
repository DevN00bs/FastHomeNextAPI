from mongoengine import *
from apiflask.fields import String, Float, Integer
from apiflask import Schema

# PropertyDoc - old PropertyCreate


class PropertyDoc(Document):
    address = StringField(unique=True)
    description = StringField()
    price = DecimalField()
    terrain_height = DecimalField()
    terrain_width = DecimalField()
    bed = IntField()
    bath = DecimalField()
    floors = IntField()
    garage = IntField()
    photo_list = ListField()
    contract = StringField()
    currency = StringField()
    meta = {"collection": "properties"}


class PropertyRead(Schema):
    id = String()
    address = String()
    description = String()
    price = Float()
    terrain_height = Float()
    terrain_width = Float()
    bed = Integer()
    bath = Float()
    floors = Integer()
    garage = Integer()
    contract = String()
    currency = String()


class NewProperty(Schema):
    address = String(required=True)
    description = String(required=True)
    price = Float(required=True)
    terrain_height = Float(required=True)
    terrain_width = Float(required=True)
    bed = Integer(required=True)
    bath = Float(required=True)
    floors = Integer(required=True)
    garage = Integer(required=True)
    contract = String(required=True)
    currency = String(required=True)


class PropertyUpdate(Schema):
    id = String(required=True)
    address = String()
    description = String()
    price = Float()
    terrain_height = Float()
    terrain_width = Float()
    bed = Integer()
    bath = Float()
    floors = Integer()
    garage = Integer()
    contract = String()
    currency = String()


class PropertyDelete(Schema):
    id = String(required=True)
