from os import environ

from apiflask.security import HTTPTokenAuth
from jwt import decode, InvalidTokenError

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    try:
        return decode(token, environ["JWT_SECRET"], ["HS256"], audience="login")
    except InvalidTokenError:
        return False
