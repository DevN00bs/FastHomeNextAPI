from typing import get_args

import mongoengine as m
from apiflask import Schema
from apiflask.fields import String, Float, Integer, Nested, Raw, List, Function, Decimal
from apiflask.validators import Length, Range, OneOf, Regexp
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
    phone_number = Function(lambda prop: prop.profile.phone_number)
    contact_email = Function(lambda prop: prop.profile.contact_email)
    facebook_link = Function(lambda prop: prop.profile.facebook_link)
    instagram_link = Function(lambda prop: prop.profile.instagram_link)
    twitter_link = Function(lambda prop: prop.profile.twitter_link)


class PropertyDoc(m.Document):
    address = m.StringField()
    description = m.StringField()
    price = m.DecimalField()
    terrain_height = m.DecimalField()
    terrain_width = m.DecimalField()
    bedrooms_amount = m.IntField()
    bathrooms_amount = m.DecimalField()
    floors_amount = m.IntField()
    garage_size = m.IntField()
    photo_list = m.EmbeddedDocumentListField(PropertyPhoto, max_length=10)
    contract_type = m.StringField()
    currency_code = m.StringField()
    owner = m.ReferenceField(User, reverse_delete_rule=m.CASCADE)
    meta = {"collection": "properties"}


class PropertyDataResponse(FilteredSchema):
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
    owner = Nested(PropertyOwnerInfo, data_key="owner_info")
    photo_ids = Function(lambda prop: [str(doc.photo.grid_id) for doc in prop.photo_list])


class PropertyDataRequest(Schema):
    id = String(required=True, validate=is_valid_id, data_key="property_id")


class BasicPropertyRead(Schema):
    id = String(data_key="property_id")
    address = String()
    price = Float()
    terrain_height = Float()
    terrain_width = Float()
    bedrooms_amount = Integer()
    bathrooms_amount = Float()
    floors_amount = Integer()
    garage_size = Integer()
    contract_type = String()
    currency_code = String()
    owner_username = Function(lambda prop: prop.owner.username)
    thumbnail_id = Function(
        lambda prop: str(prop.photo_list.first().photo.thumbnail._id) if prop.photo_list.first() is not None else None)


class NewProperty(Schema):
    address = String(required=True, validate=Length(1, 150))
    description = String(validate=Length(max=2000))
    price = Decimal(required=True, places=4, validate=Range(1, 999_999_999.9999))
    terrain_height = Decimal(required=True, places=2, validate=Range(1, 999.99))
    terrain_width = Decimal(required=True, places=2, validate=Range(1, 999.99))
    bedrooms_amount = Integer(strict=True, required=True, validate=Range(1, 99))
    bathrooms_amount = Decimal(required=True, places=1, validate=Range(1, 99.5))
    floors_amount = Integer(strict=True, required=True, validate=Range(1, 99))
    garage_size = Integer(strict=True, required=True, validate=Range(1, 99))
    contract_type = String(required=True, validate=OneOf(get_args(contract_types)))
    currency_code = String(required=True, validate=Length(3, 3))


class NewPropertyResponse(Schema):
    id = String(data_key="property_id")


class PropertyUpdate(Schema):
    id = String(required=True, validate=is_valid_id, data_key="property_id")
    address = String(validate=Length(1, 150))
    description = String(validate=Length(max=2000))
    price = Decimal(places=4, validate=Range(1, 999_999_999.9999))
    terrain_height = Decimal(places=2, validate=Range(1, 999.99))
    terrain_width = Decimal(places=2, validate=Range(1, 999.99))
    bedrooms_amount = Integer(strict=True, validate=Range(1, 99))
    bathrooms_amount = Decimal(places=1, validate=Range(1, 99.5))
    floors_amount = Integer(strict=True, validate=Range(1, 99))
    garage_size = Integer(strict=True, validate=Range(1, 99))
    contract_type = String(validate=OneOf(get_args(contract_types)))
    currency_code = String(validate=Length(3, 3))


class PropertyDelete(Schema):
    id = String(required=True, validate=is_valid_id, data_key="property_id")


class UploadPhotosQueryRequest(Schema):
    id = String(required=True, validate=is_valid_id, data_key="property_id")


class UploadPhotosFilesRequest(Schema):
    main_photo = Raw(type="string", format="binary", required=True)
    photos = List(Raw(type="string", format="binary"), validate=Length(max=9))


class UploadPhotosRequest(Schema):
    property_id = String()
    main_photo = Raw(type="string", format="binary")
    photos = List(Raw(type="string", format="binary"), validate=Length(max=9))


class PropertyOptionsRequest(Schema):
    bedrooms_amount = String(validate=Regexp(r"^[1-9]\d*\+?$"))
    bathrooms_amount = String(validate=Regexp(r"^[1-9]\d*(\.5)?\+?$"),
                              metadata={"description": ".5 represents half bathrooms"})
    floors_amount = String(validate=Regexp(r"^[1-9]\d*\+?$"))
    garage_size = String(validate=Regexp(r"^[1-9]\d*\+?$"))
    page_number = Integer(required=True, validate=Range(1, 999))
    per_page = Integer(required=True, validate=Range(1, 99))
