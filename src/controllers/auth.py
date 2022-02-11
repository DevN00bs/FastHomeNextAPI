from mongoengine.errors import OperationError, NotUniqueError
from werkzeug.security import generate_password_hash

from ..models.auth import User
from ..utils.enums import ControllerStatus


def register_user(data) -> ControllerStatus:
    hashed_passwd = generate_password_hash(data["password"])
    try:
        User(
            username=data["username"],
            passwd_hash=hashed_passwd,
            email=data["email"]
        ).save()
        return ControllerStatus.SUCCESS
    except NotUniqueError:
        return ControllerStatus.ALREADY_EXISTS
    except OperationError:
        return ControllerStatus.ERROR
