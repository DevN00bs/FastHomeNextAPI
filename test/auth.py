from os import environ
from unittest import TestCase

from jwt import decode
from mongoengine import connect, disconnect
from werkzeug.security import generate_password_hash

from src.controllers.auth import log_in
from src.models.auth import User
from src.utils.enums import ControllerStatus


class LoginTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        User(
            username="testuser",
            email="test@example.net",
            passwd_hash=generate_password_hash("testpass")
        ).save()

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect()

    @staticmethod
    def test_successful_login():
        tuple_result = log_in({
            "username": "testuser",
            "password": "testpass"
        })

        assert tuple_result[0] == ControllerStatus.SUCCESS and str(User.objects(username="testuser").first().id) == \
               decode(
                   tuple_result[1], environ["JWT_SECRET"], ["HS256"], audience="login")["id"]
