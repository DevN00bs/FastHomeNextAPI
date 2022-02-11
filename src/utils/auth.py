from os import environ

from apiflask.security import HTTPTokenAuth
from jwt import decode

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    return decode(token, environ["JWT_SECRET"], ["HS256"])
