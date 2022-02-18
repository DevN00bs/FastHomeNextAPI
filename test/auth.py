from os import environ
from unittest import TestCase

from jwt import decode
from mongoengine import connect, disconnect
from werkzeug.security import generate_password_hash

from src.controllers.auth import log_in, register_user
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

    def test_wrong_username(self):
        tuple_result = log_in({
            "username": "wronguser",
            "password": self._password
        })

        assert tuple_result[0] == ControllerStatus.WRONG_CREDS

    def test_wrong_password(self):
        tuple_result = log_in({
            "username": self._username,
            "password": "wrongpass"
        })

        assert tuple_result[0] == ControllerStatus.WRONG_CREDS

    def test_successful_registration(self):
        result = register_user({
            "username": "newuser",
            "email": "new@example.net",
            "password": self._password
        })

        assert result[0] == ControllerStatus.SUCCESS

    def test_repeated_username(self):
        result = register_user({
            "username": self._username,
            "email": "new@example.net",
            "password": self._password
        })
        
        assert result[0] == ControllerStatus.ALREADY_EXISTS

    def test_repeated_email(self):
        result = register_user({
            "username": "newuser",
            "email": self._email,
            "password": self._password
        })
        
        assert result[0] == ControllerStatus.ALREADY_EXISTS
