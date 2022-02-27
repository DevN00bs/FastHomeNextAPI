from mongoengine.errors import OperationError, DoesNotExist

# Import src.models.properties as prop
import src.models.profiles as prof
from ..utils.enums import ControllerStatus
from ..utils.auth import auth

# Get the user profile
# I need help on knowing how to bring the id by clicking
# A "property" so it can be taken there from it xD


def read_prof(user_id) -> ControllerStatus:
    try:
        prof_id = prof.ProfileDoc.objects.get()
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    # Here instead of current, goes owner and uncomment prop owner above
    if user_id["id"] == prof_id["user"].id:

        return prof.ProfileDoc.objects


# Update profile - owner like field to be created, idk what to do


def update_prof(data, user_id) -> ControllerStatus:
    prof_info = prof.ProfileDoc

    if str(user_id == auth.current_user):
        try:
            if data["phone"] == "string":
                prof_info(
                    **data,
                    user=user_id
                    ).save()
            else:
                prof_info.objects.update(**data)
        except OperationError:
            return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
