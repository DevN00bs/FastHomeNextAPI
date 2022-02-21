from mongoengine.errors import OperationError

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


def all_props() -> tuple[ControllerStatus, list[m.NewProperty]]:
    try:
        data = m.PropertyDoc.objects
        # Objects means all data in the db + (filters)
        return ControllerStatus.SUCCESS, data
    except OperationError:
        return ControllerStatus.ERROR, list()
        # When create, parenthesis; read, brackets


def update_prop(data) -> ControllerStatus:
    try:
        m.PropertyDoc.objects(id=data["id"]).first().update(**data)  # Schema
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR


def delete_prop(data) -> ControllerStatus:
    try:
        m.PropertyDoc.objects(id=data["id"]).first().delete()
        # First to avoid making useless lists
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR
