from mongoengine.errors import OperationError
from werkzeug.security import generate_password_hash

from ..models.auth import User


def register_user(data) -> bool:
    hashed_passwd = generate_password_hash(data["password"])
    try:
        User(
            username=data["username"],
            passwd_hash=hashed_passwd,
            email=data["email"]
        ).save()
        return True
    except OperationError:
        return False
