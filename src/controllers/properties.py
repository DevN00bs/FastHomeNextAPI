from mongoengine.errors import OperationError

from ..models.properties import *
from ..utils.enums import ControllerStatus

def register_prop(data) -> ControllerStatus:
    try:
        PropertyCreate(
            **data
        ).save()
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR

def all_props(data) -> tuple[ControllerStatus, list[PropertyRead]]:
    try:
        data = PropertyRead.objects #objects means all data in the db + (filters)
        return ControllerStatus.SUCCESS, data
    except OperationError:
        return ControllerStatus.ERROR, list() #when create, parenthesis; read, brackets

def update_prop(data) -> ControllerStatus:
    try:
        PropertyUpdate.objects(id=data["id"]).first().update(**data) #depends on the schema
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR

def delete_prop(data) -> ControllerStatus:
    try:
        PropertyDelete.objects(id=data["id"]).first().delete() #first to avoid making useless lists
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR
