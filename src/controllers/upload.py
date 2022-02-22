from mongoengine import DoesNotExist, OperationError
from werkzeug.datastructures import FileStorage

from ..models.properties import PropertyDoc, PropertyPhoto
from ..utils.enums import ControllerStatus


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
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
