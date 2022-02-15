from mongoengine.errors import OperationError

from ..models.properties import PropertyData
from ..utils.enums import ControllerStatus


# create
def register_prop(data) -> ControllerStatus:
    try:
        PropertyData(
            **data
        ).save()
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR


# read
def all_props(data) -> ControllerStatus:
    try:
        prop_data = PropertyData.objects(address=data["address"])  # just saved cuz maybe used later
        PropertyData(
            **data
        ).get_collection(meta={"collection": "properties"})
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR


# TODO: field search

# update
def update_prop(data) -> ControllerStatus:
    try:
        PropertyData(
            **data
        ).update()
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR


# delete
def delete_prop(data) -> ControllerStatus:
    try:
        PropertyData(
            **data
        ).delete()
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR
