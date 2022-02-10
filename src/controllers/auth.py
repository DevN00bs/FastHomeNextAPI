from ..models.auth import RegistrationRequest, User
from werkzeug.security import generate_password_hash
from mongoengine.errors import OperationError


def register_user(data: RegistrationRequest) -> bool:
    hashed_passwd = generate_password_hash(data.password)
    try:
        User(**data.__dict__, passwdHash=hashed_passwd).save()
        return True
    except OperationError:
        return False
