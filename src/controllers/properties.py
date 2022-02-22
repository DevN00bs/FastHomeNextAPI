from mongoengine.errors import OperationError, DoesNotExist

import src.models.properties as m
from ..utils.enums import ControllerStatus


def register_prop(data, user_id) -> tuple[ControllerStatus, str]:
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
        required_prop.delete()
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
