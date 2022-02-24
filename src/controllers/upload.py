from typing import Optional

from bson import ObjectId
from mongoengine import DoesNotExist, OperationError, ImageGridFsProxy, ValidationError
from werkzeug.datastructures import FileStorage

from ..models.properties import PropertyDoc, PropertyPhoto
from ..utils.enums import ControllerStatus
from ..utils.types import allowed_mimetypes


def check_file_type(photos: list[FileStorage]) -> ControllerStatus:
    for photo in photos:
        if photo.mimetype not in allowed_mimetypes:
            return ControllerStatus.NOT_AN_IMAGE

    return ControllerStatus.SUCCESS


def upload_properties_photos(prop_id: str, user_id: str, photos: list[FileStorage]) -> ControllerStatus:
    try:
        requested_prop: PropertyDoc = PropertyDoc.objects.get(id=prop_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(requested_prop.owner.id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        for photo in photos:
            new_doc: PropertyPhoto = requested_prop.photo_list.create()
            new_doc.photo.put(photo)
            new_doc.photo.name = f"{new_doc.photo.grid_id}.{photo.filename.split('.').pop()}"

        requested_prop.save()
    except ValidationError:
        return ControllerStatus.NOT_AN_IMAGE
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS


def get_photo_from_db(photo_id: str) -> tuple[ControllerStatus, Optional[ImageGridFsProxy]]:
    photo = ImageGridFsProxy(ObjectId(photo_id), "photo", collection_name="photos")
    if photo.format is None:
        return ControllerStatus.DOES_NOT_EXISTS, None

    return ControllerStatus.SUCCESS, photo
