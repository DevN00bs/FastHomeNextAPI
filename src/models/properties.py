import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Float, Integer


# PropertyDoc - old PropertyCreate


class PropertyDoc(m.Document):
    address = m.StringField(unique=True)
    description = m.StringField()
    price = m.DecimalField()
    terrain_height = m.DecimalField()
    terrain_width = m.DecimalField()
    bed = m.IntField()
    bath = m.DecimalField()
    floors = m.IntField()
    garage = m.IntField()
    photo_list = m.ListField()
    contract = m.StringField()
    currency = m.StringField()
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
