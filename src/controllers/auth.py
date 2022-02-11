from mongoengine.errors import OperationError, NotUniqueError
from werkzeug.security import generate_password_hash, check_password_hash

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


def log_in(data):
    try:
        user_data = User.objects(username=data["username"]).first()
    except OperationError:
        return ControllerStatus.ERROR

    if user_data is None:
        return ControllerStatus.WRONG_CREDS

    if not user_data["is_verified"]:
        return ControllerStatus.NOT_VERIFIED

    if not check_password_hash(user_data["passwd_hash"], data["password"]):
        return ControllerStatus.WRONG_CREDS

    return ControllerStatus.SUCCESS
