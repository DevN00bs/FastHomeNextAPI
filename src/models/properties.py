from typing import get_args

import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Float, Integer, Nested, Raw, List, Function, Decimal
from apiflask.validators import Length, Range, OneOf
from marshmallow import post_dump

from ..models.auth import User
from ..utils.types import is_valid_id, contract_types


class FilteredSchema(Schema):
    VALUES_TO_FILTER = [None, ""]

    @post_dump
    def remove_none(self, data, **_kwargs):
        return {
            key: value for key, value in data.items()
            if value not in self.VALUES_TO_FILTER
        }


class PropertyPhoto(m.EmbeddedDocument):
    photo = m.ImageField(size=(1280, 720, True), thumbnail_size=(640, 360, True), collection_name="photos")


class PropertyOwnerInfo(FilteredSchema):
    username = String()
    phone = Function(lambda prop: prop.profile.phone)
    contact_email = Function(lambda prop: prop.profile.contact_email)
    fb_link = Function(lambda prop: prop.profile.fb_link)
    insta_link = Function(lambda prop: prop.profile.insta_link)
    twit_link = Function(lambda prop: prop.profile.twit_link)


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


class PropertyDataResponse(FilteredSchema):
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
    owner = Nested(PropertyOwnerInfo, data_key="owner_info")
    photo_ids = Function(lambda prop: [str(doc.photo.grid_id) for doc in prop.photo_list])


class PropertyDataRequest(Schema):
    id = String(required=True, validate=is_valid_id)


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
    address = String(required=True, validate=Length(1, 150))
    description = String(validate=Length(max=2000))
    price = Decimal(required=True, places=4, validate=Range(1, 999_999_999.9999))
    terrain_height = Decimal(required=True, places=2, validate=Range(1, 999.99))
    terrain_width = Decimal(required=True, places=2, validate=Range(1, 999.99))
    bed = Integer(strict=True, required=True, validate=Range(1, 99))
    bath = Decimal(required=True, places=1, validate=Range(1, 99.5))
    floors = Integer(strict=True, required=True, validate=Range(1, 99))
    garage = Integer(strict=True, required=True, validate=Range(1, 99))
    contract = String(required=True, validate=OneOf(get_args(contract_types)))
    currency = String(required=True, validate=Length(3, 3))


class NewPropertyResponse(Schema):
    id = String()


class PropertyUpdate(Schema):
    id = String(required=True, validate=is_valid_id)
    address = String(validate=Length(1, 150))
    description = String(validate=Length(max=2000))
    price = Decimal(places=4, validate=Range(1, 999_999_999.9999))
    terrain_height = Decimal(places=2, validate=Range(1, 999.99))
    terrain_width = Decimal(places=2, validate=Range(1, 999.99))
    bed = Integer(strict=True, validate=Range(1, 99))
    bath = Decimal(places=1, validate=Range(1, 99.5))
    floors = Integer(strict=True, validate=Range(1, 99))
    garage = Integer(strict=True, validate=Range(1, 99))
    contract = String(validate=OneOf(get_args(contract_types)))
    currency = String(validate=Length(3, 3))


class PropertyDelete(Schema):
    id = String(required=True, validate=is_valid_id)


class UploadPhotosQueryRequest(Schema):
    id = String(required=True, validate=is_valid_id)


class UploadPhotosFilesRequest(Schema):
    main_photo = Raw(type="string", format="binary", required=True)
    photos = List(Raw(type="string", format="binary"), validate=Length(max=9))


class UploadPhotosRequest(Schema):
    id = String()
    main_photo = Raw(type="string", format="binary")
    photos = List(Raw(type="string", format="binary"), validate=Length(max=9))
