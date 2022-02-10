from os import environ

from apiflask import APIFlask
from mongoengine import connect

app = APIFlask(__name__,
               title="FastHome API",
               version="0.1.0.alpha")
connect(
    host=environ["DB_HOST"],
    username=environ["DB_USER"],
    password=environ["DB_PASS"],
    db=environ["DB_NAME"]
)
