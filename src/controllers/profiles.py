# Controllers - otros users pueden ver profiles
from mongoengine.errors import OperationError, DoesNotExist

import src.models.profiles as m
from ..utils.enums import ControllerStatus

# Get the user profile - idk if it stills a tuple


def read_prof(data, user_id) -> ControllerStatus:
    try:
        req_prof = m.ProfileDoc.objects.get(id=data["id"])
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(req_prof.id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        return ControllerStatus.SUCCESS
    except OperationError:
        return ControllerStatus.ERROR, ""


# Update profile - owner like field to be created, idk what to do


def update_prof(data, user_id) -> ControllerStatus:
    try:
        req_prof = m.ProfileDoc.objects.get(id=data["id"])
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(req_prof.id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        req_prof.update(**data)
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS


# Delete profile - NOT YET

'''
def delete_prof(data, user_id) -> ControllerStatus:
    try:
        req_prof = m.ProfileDoc.objects.get(id=data["id"])
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(req_prof["owner"].id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        req_prof.delete()
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
'''
