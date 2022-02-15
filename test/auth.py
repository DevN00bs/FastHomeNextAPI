from os import environ
from unittest import TestCase

from jwt import decode
from mongoengine import connect, disconnect
from werkzeug.security import generate_password_hash

from src.controllers.auth import log_in
from src.models.auth import User
from src.utils.enums import ControllerStatus


class AuthTests(TestCase):
    _username = "testuser"
    _password = "testpass"
    _email = "test@example.net"

    @classmethod
    def setUpClass(cls) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        User(
            username=cls._username,
            email=cls._email,
            passwd_hash=generate_password_hash(cls._password)
        ).save()

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect()

    def test_successful_login(self):
        tuple_result = log_in({
            "username": self._username,
            "password": self._password
        })

        assert tuple_result[0] == ControllerStatus.SUCCESS and str(User.objects(username=self._username).first().id) == \
               decode(tuple_result[1], environ["JWT_SECRET"], ["HS256"], audience="login")["id"]
