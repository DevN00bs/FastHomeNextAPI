from typing import Optional

from mongoengine.errors import OperationError, DoesNotExist

import fast_home_api.models.properties as m
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


def all_props(options: dict[str, any]) -> tuple[ControllerStatus, list[m.PropertyDoc]]:
    per_page = options["per_page"]
    starting_point = (options["page_number"] - 1) * per_page
    finish_point = starting_point + per_page
    try:
        return ControllerStatus.SUCCESS, m.PropertyDoc.objects[starting_point: finish_point](**{
            f"{field}{'__gte' if value.endswith('+') else ''}": float(value.rstrip("+")) for field, value in
            {field: value for field, value in options.items() if type(value) == str}.items()
        })
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
