from os import environ
from unittest import TestCase

from jwt import decode
from mongoengine import connect, disconnect
from werkzeug.security import generate_password_hash

from src.controllers.auth import log_in, register_user
from src.models.auth import User
from src.utils.enums import ControllerStatus


class LoginTests(TestCase):
    _password = "testpass"
    _email = "test@example.net"
    _new_user = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": _email,
        "profile": {
            "contact_email": _email
        }
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        User(**self._new_user).save()

    def tearDown(self) -> None:
        disconnect()

    def test_successful_login(self):
        tuple_result = log_in({
            "username": self._new_user["username"],
            "password": self._password
        })

        self.assertEqual(tuple_result[0], ControllerStatus.SUCCESS)
        self.assertEqual(str(User.objects(username=self._new_user["username"]).first().id),
                         decode(tuple_result[1], environ["JWT_SECRET"], ["HS256"], audience="login")["id"])

    def test_wrong_username(self):
        tuple_result = log_in({
            "username": "wronguser",
            "password": self._password
        })

        self.assertEqual(tuple_result[0], ControllerStatus.WRONG_CREDS)

    def test_wrong_password(self):
        tuple_result = log_in({
            "username": self._new_user["username"],
            "password": "wrongpass"
        })

        self.assertEqual(tuple_result[0], ControllerStatus.WRONG_CREDS)


class RegisterTests(TestCase):
    _new_user = {
        "username": "newuser",
        "email": "new@example.net",
        "password": "testpass"
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")

    def tearDown(self) -> None:
        disconnect()

    def test_successful_registration(self):
        result = register_user(self._new_user)

        self.assertEqual(result[0], ControllerStatus.SUCCESS)
        self.assertEqual(User.objects.get(username=self._new_user["username"]).email, self._new_user["email"])

    def test_repeated_username(self):
        User(username=self._new_user["username"], passwd_hash=generate_password_hash(self._new_user["password"]),
             email=self._new_user["email"]).save()
        result = register_user({
            **self._new_user,
            "email": "otheraddress@example.net"
        })

        self.assertEqual(result[0], ControllerStatus.ALREADY_EXISTS)
        self.assertEqual(len(User.objects(username=self._new_user["username"])), 1)

    def test_repeated_email(self):
        User(username=self._new_user["username"], passwd_hash=generate_password_hash(self._new_user["password"]),
             email=self._new_user["email"]).save()
        result = register_user({
            **self._new_user,
            "username": "notthesame"
        })

        self.assertEqual(result[0], ControllerStatus.ALREADY_EXISTS)
        self.assertEqual(len(User.objects(email=self._new_user["email"])), 1)
