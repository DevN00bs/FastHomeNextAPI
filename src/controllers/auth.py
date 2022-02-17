from os import environ

from jwt import encode, decode, InvalidTokenError
from mongoengine.errors import OperationError, NotUniqueError, DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.auth import User
from ..utils.enums import ControllerStatus


def register_user(data) -> tuple[ControllerStatus, str]:
    hashed_passwd = generate_password_hash(data["password"])
    try:
        new_user = User(
            username=data["username"],
            passwd_hash=hashed_passwd,
            email=data["email"]
        ).save()
        return ControllerStatus.SUCCESS, str(new_user.id)
    except NotUniqueError:
        return ControllerStatus.ALREADY_EXISTS, ""
    except OperationError:
        return ControllerStatus.ERROR, ""


def log_in(data) -> tuple[ControllerStatus, str]:
    try:
        user_data = User.objects(username=data["username"]).first()
    except OperationError:
        return ControllerStatus.ERROR, ""

    if user_data is None:
        return ControllerStatus.WRONG_CREDS, ""

    if not user_data["is_verified"]:
        return ControllerStatus.NOT_VERIFIED, ""

    if not check_password_hash(user_data["passwd_hash"], data["password"]):
        return ControllerStatus.WRONG_CREDS, ""

    return ControllerStatus.SUCCESS, encode({"id": str(user_data.id), "aud": "login"}, environ["JWT_SECRET"])


def verify_token(token: str) -> ControllerStatus:
    try:
        token_data = decode(token, environ["JWT_SECRET"], ["HS256"], audience="verify")
    except InvalidTokenError:
        return ControllerStatus.INVALID_LINK

    try:
        User.objects.get(id=token_data["id"]).update(is_verified=True)
    except DoesNotExist:
        return ControllerStatus.INVALID_LINK
    except OperationError:
        return ControllerStatus.ERROR

    return ControllerStatus.SUCCESS
