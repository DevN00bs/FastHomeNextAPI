import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Float, Integer, Nested, Raw, List, Function
from apiflask.validators import Length

from ..models.auth import User, PropertyOwnerInfo


class PropertyPhoto(m.EmbeddedDocument):
    photo = m.ImageField(size=(1280, 720, True), thumbnail_size=(640, 360, True), collection_name="photos")


class PropertyDoc(m.Document):
    address = m.StringField()
    description = m.StringField()
    price = m.DecimalField()
    terrain_height = m.DecimalField()
    terrain_width = m.DecimalField()
    bed = m.IntField()
    bath = m.DecimalField()
    floors = m.IntField()
    garage = m.IntField()
    photo_list = m.EmbeddedDocumentListField(PropertyPhoto, max_length=10)
    contract = m.StringField()
    currency = m.StringField()
    owner = m.ReferenceField(User, reverse_delete_rule=m.CASCADE)
    meta = {"collection": "properties"}


class BasicPropertyRead(Schema):
    id = String(data_key="property_id")
    address = String()
    price = Float()
    terrain_height = Float()
    terrain_width = Float()
    bed = Integer()
    bath = Float()
    floors = Integer()
    garage = Integer()
    contract = String()
    currency = String()
    owner_username = Function(lambda prop: prop.owner.username)
    thumbnail_id = Function(lambda prop: str(prop.photo_list.first().photo.thumbnail._id))


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


class NewPropertyResponse(Schema):
    id = String()


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


class UploadPhotosQueryRequest(Schema):
    id = String(required=True)


class UploadPhotosFilesRequest(Schema):
    main_photo = Raw(type="string", format="binary", required=True)
    photos = List(Raw(type="string", format="binary"), validate=Length(max=9))


class UploadPhotosRequest(Schema):
    id = String()
    main_photo = Raw(type="string", format="binary")
    photos = List(Raw(type="string", format="binary"), validate=Length(max=9))
