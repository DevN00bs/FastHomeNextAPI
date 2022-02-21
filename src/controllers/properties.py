from mongoengine.errors import OperationError, DoesNotExist

import src.models.properties as m
from ..utils.enums import ControllerStatus


def register_prop(data, user_id) -> ControllerStatus:
    try:
        m.PropertyDoc(
            **data,
            owner=user_id
        ).save()
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR


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


def delete_prop(data) -> ControllerStatus:
    try:
        m.PropertyDoc.objects(id=data["id"]).first().delete()
        # First to avoid making useless lists
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR
