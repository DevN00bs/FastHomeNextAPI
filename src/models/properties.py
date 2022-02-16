from mongoengine import Document, StringField, DecimalField, IntField, ListField
from apiflask.fields import String, Float, Integer, UUID
from apiflask import Schema

class PropertyCreate(Document):
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

#required has to have data; depends on how front makes it able to be editable, might delete some required
class PropertyUpdate(Schema):
    id = UUID(default=True)
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

class PropertyDelete(Schema):
    id = UUID(default=True)
