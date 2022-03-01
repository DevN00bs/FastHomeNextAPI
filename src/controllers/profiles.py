from mongoengine.errors import OperationError, DoesNotExist

# Import src.models.properties as prop
import src.models.auth as prof
from src.models.profiles import ProfileDoc
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
        prof_info = prof.User.objects.get(id=user_id)
        for field, value in data.items():
            prof_info.profile[field] = value
        prof_info.save()

    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
