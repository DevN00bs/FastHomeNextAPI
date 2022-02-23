# Controllers - otros users pueden ver profiles
from mongoengine.errors import OperationError, DoesNotExist

import src.models.profiles as m
from ..utils.enums import ControllerStatus

# Get the one clicked


# Get the user profile


# Update profile - auth usr req on req_prof


def update_prof(data, user_id) -> ControllerStatus:
    try:
        req_prof = m.ProfileDoc.objects.get(id=data["id"])
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    if str(req_prof["owner"].id) != user_id:
        return ControllerStatus.UNAUTHORIZED

    try:
        req_prof.update(**data)
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS


# Delete profile - auth req - "owner" question


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
