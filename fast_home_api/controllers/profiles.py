from mongoengine.errors import OperationError, DoesNotExist

import fast_home_api.models.properties as prop
import fast_home_api.models.auth as prof
from ..utils.enums import ControllerStatus
from typing import Any


def read_prof(user_id) -> tuple[ControllerStatus, dict[str, Any]]:
    try:
        props = prop.PropertyDoc.objects(owner=user_id)
        prof_id = prof.User.objects.get(id=user_id).profile
    except DoesNotExist:
        return ControllerStatus.DOES_NOT_EXISTS, {}
    except OperationError:
        return ControllerStatus.ERROR, {}

    return ControllerStatus.SUCCESS, {**prof_id.to_mongo().to_dict(), "properties_list": list(props)}


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
