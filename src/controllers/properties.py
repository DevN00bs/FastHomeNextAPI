from typing import Optional

from mongoengine.errors import OperationError, DoesNotExist

import src.models.properties as m
import src.models.auth as usr
from ..utils.enums import ControllerStatus


def register_prop(data, user_id) -> tuple[ControllerStatus, str]:
    if str(usr.User.objects.get().id) != user_id:
        return ControllerStatus.DOES_NOT_EXISTS, ""

    try:
        new_prop = m.PropertyDoc(
            **data,
            owner=user_id
        ).save()
        return ControllerStatus.SUCCESS, str(new_prop.id)
    except OperationError:
        return ControllerStatus.ERROR, ""


def all_props() -> tuple[ControllerStatus, list[m.PropertyDoc]]:
    try:
        return ControllerStatus.SUCCESS, m.PropertyDoc.objects
    except OperationError:
        return ControllerStatus.ERROR, list()


def update_prop(data, user_id) -> ControllerStatus:
    try:
        requested_prop = m.PropertyDoc.objects.get(id=data["id"])
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(requested_prop["owner"].id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        requested_prop.update(**data)
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS


def delete_prop(data, user_id) -> ControllerStatus:
    try:
        required_prop = m.PropertyDoc.objects.get(id=data["id"])
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(required_prop["owner"].id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        for doc in required_prop.photo_list:
            doc.photo.delete()

        required_prop.delete()
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS


def get_property_data(prop_id: str) -> tuple[ControllerStatus, Optional[m.PropertyDoc]]:
    try:
        requested_prop = m.PropertyDoc.objects.get(id=prop_id)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, None
    except OperationError:
        return ControllerStatus.ERROR, None

    return ControllerStatus.SUCCESS, requested_prop
