from unittest import TestCase

from mongoengine import connect, disconnect, DoesNotExist
from werkzeug.security import generate_password_hash

import fast_home_api.controllers.profiles as profile
from fast_home_api.models.auth import User
from fast_home_api.utils.enums import ControllerStatus


class ReadProfileTests(TestCase):
    _password = "testpass"
    _user_object = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": "test@example.net",
        "profile": {
            "contact_email": "contact@example.net",
            "phone_number": "+18742548811",
            "facebook_link": "https://facebook.com/test.user",
            "twitter_link": "https://twitter.com/test_user",
            "instagram_link": "https://instagram.com/test.user"
        }
    }
    _id = ""

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._user_object).save()
        self._id = str(new_user.id)

    def tearDown(self) -> None:
        disconnect()

    def test_successful_get_profile_data(self):
        result = profile.read_prof(self._id)

        self.assertDictEqual(result.to_mongo().to_dict(), self._user_object["profile"])
        self.assertDictEqual(self._user_object["profile"], User.objects.get(id=self._id).profile.to_mongo().to_dict())

    def test_user_not_found(self):
        testing_id = "621ff445fffa26ca23ba651b"
        result = profile.read_prof(testing_id)

        self.assertEqual(result, ControllerStatus.DOES_NOT_EXISTS)
        self.assertRaises(DoesNotExist, lambda: User.objects.get(id=testing_id))


class UpdateProfileTests(TestCase):
    _password = "testpass"
    _user_object = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": "test@example.net",
        "profile": {
            "contact_email": "contact@example.net",
            "phone_number": "+18742548811",
            "facebook_link": "https://facebook.com/test.user",
            "twitter_link": "https://twitter.com/test_user",
            "instagram_link": "https://instagram.com/test.user"
        }
    }
    _id = ""

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._user_object).save()
        self._id = str(new_user.id)

    def tearDown(self) -> None:
        disconnect()

    def test_successful_profile_update(self):
        new_profile_info = {
            "contact_email": "newmail@example.com",
            "phone_number": "+77415239674"
        }
        result = profile.update_prof(new_profile_info, self._id)

        self.assertEqual(result, ControllerStatus.SUCCESS)
        self.assertDictEqual(User.objects.get(id=self._id).profile.to_mongo().to_dict(),
                             {**self._user_object["profile"], **new_profile_info})

    def test_user_not_found(self):
        testing_id = "621ff445fffa26ca23ba651b"
        result = profile.update_prof({}, testing_id)

        self.assertEqual(result, ControllerStatus.DOES_NOT_EXISTS)
        self.assertRaises(DoesNotExist, lambda: User.objects.get(id=testing_id))
