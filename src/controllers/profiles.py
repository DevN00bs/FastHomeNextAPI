from mongoengine.errors import OperationError, DoesNotExist

# Import src.models.properties as prop
import src.models.auth as prof
from ..utils.enums import ControllerStatus

# Get the user profile
# I need help on knowing how to bring the id by clicking
# A "property" so it can be taken there from it xD


def read_prof(user_id) -> ControllerStatus:
    try:
        prof_id = prof.User.objects.get(id=user_id).profile
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    return prof_id


def update_prof(data, user_id) -> ControllerStatus:

    try:
        prof.User.objects.get(id=user_id).profile.update(**data)
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
