from mongoengine.errors import OperationError, DoesNotExist

import src.models.profiles as m
from ..utils.enums import ControllerStatus
from ..utils.auth import auth

# Get the user profile - idk if it stills a tuple


def read_prof() -> ControllerStatus:
    try:
        return ControllerStatus.SUCCESS, m.ProfileDoc.objects
    except OperationError:
        return ControllerStatus.ERROR


# Update profile - owner like field to be created, idk what to do


def update_prof(data, user_id) -> ControllerStatus:
    prof_info = m.ProfileDoc

    if str(user_id == auth.current_user):
        try:
            if data["phone"] == "string":
                try:
                    prof_info(
                        **data,
                        user=user_id
                        ).save()
                except OperationError:
                    return ControllerStatus.ERROR
            else:
                try:
                    prof_info.objects.update(**data)
                except OperationError:
                    return ControllerStatus.ERROR
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
