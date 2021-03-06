from unittest import TestCase

from mongoengine import connect, disconnect, DoesNotExist
from werkzeug.security import generate_password_hash

from fast_home_api.controllers.properties import register_prop, all_props, update_prop, delete_prop, get_property_data
from fast_home_api.models.auth import User
from fast_home_api.models.properties import PropertyDoc
from fast_home_api.utils.enums import ControllerStatus


class CreatePropertyTests(TestCase):
    _email = "test@example.net"
    _password = "testpass"
    _id = ""
    _register_user = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": _email,
        "profile": {
            "contact_email": _email
        }
    }
    _new_prop = {
        "address": "1234 Test Street",
        "bathrooms_amount": 1.5,
        "bedrooms_amount": 3,
        "contract_type": "rent",
        "currency_code": "EUR",
        "floors_amount": 1,
        "garage_size": 2,
        "price": 120000,
        "terrain_height": 5,
        "terrain_width": 7
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._register_user).save()
        self._id = str(new_user.id)

    def tearDown(self) -> None:
        disconnect()

    def test_successful_create_property(self):
        result = register_prop(self._new_prop, self._id)

        self.assertEqual(result[0], ControllerStatus.SUCCESS)
        self.assertEqual(PropertyDoc.objects.get(address=self._new_prop["address"]).address, self._new_prop["address"])


class GetAllPropertiesTest(TestCase):
    _email = "test@example.net"
    _password = "testpass"
    _id = ""
    _register_user = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": _email,
        "profile": {
            "contact_email": _email
        }
    }
    _register_prop = {
        "address": "1234 Test Street",
        "bathrooms_amount": 1.5,
        "bedrooms_amount": 3,
        "contract_type": "rent",
        "currency_code": "EUR",
        "floors_amount": 1,
        "garage_size": 2,
        "price": 120000,
        "terrain_height": 5,
        "terrain_width": 7
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._register_user).save()
        PropertyDoc(**self._register_prop, owner=new_user.id).save()
        self._id = str(new_user.id)

    def tearDown(self) -> None:
        disconnect()

    def test_get_properties(self):
        pagination_object = {
            "page_number": 1,
            "per_page": 1
        }
        result = all_props(pagination_object)

        self.assertEqual(result[0], ControllerStatus.SUCCESS)
        self.assertEqual(result[1].first().address, self._register_prop["address"])

    def test_filtered_property_list(self):
        options_object = {
            "bedrooms_amount": "10",
            "page_number": 1,
            "per_page": 1
        }
        extra_property_address = "748 Italien Avenue"
        PropertyDoc(**{
            "address": extra_property_address,
            "bathrooms_amount": 7,
            "bedrooms_amount": 10,
            "contract_type": "sell",
            "currency_code": "MXN",
            "floors_amount": 2,
            "garage_size": 7,
            "price": 85000000,
            "terrain_height": 47,
            "terrain_width": 50,
            "owner": self._id
        }).save()

        result = all_props(options_object)

        self.assertEqual(result[0], ControllerStatus.SUCCESS)
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1].first().address, extra_property_address)
        self.assertEqual(
            len(PropertyDoc.objects(**{field: value for field, value in options_object.items() if type(value) == str})),
            1)


class UpdatePropertyTest(TestCase):
    _email = "test@example.net"
    _password = "testpass"
    _userId = ""
    _propId = ""
    _register_user = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": _email,
        "profile": {
            "contact_email": _email
        }
    }
    _register_prop = {
        "address": "1234 Test Street",
        "bathrooms_amount": 1.5,
        "bedrooms_amount": 3,
        "contract_type": "rent",
        "currency_code": "EUR",
        "floors_amount": 1,
        "garage_size": 2,
        "price": 120000.11,
        "terrain_height": 5,
        "terrain_width": 7
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._register_user).save()
        self._userId = str(new_user.id)
        new_prop = PropertyDoc(**self._register_prop, owner=self._userId).save()
        self._propId = str(new_prop.id)

    def tearDown(self) -> None:
        disconnect()

    def test_successful_edit(self):
        _price = 10
        result = update_prop({
            "price": _price,
            "terrain_height": 2,
            "terrain_width": 3,
            "id": self._propId
        }, self._userId)

        self.assertEqual(result, ControllerStatus.SUCCESS)
        self.assertEqual(PropertyDoc.objects.get(id=self._propId).price, _price)

    def test_nonexistent_update(self):
        _price = 12
        test_id = "60999999a651cad33ea0510f"
        result = update_prop({
            "price": _price,
            "terrain_height": 2,
            "terrain_width": 3,
            "id": test_id
        }, self._userId)

        self.assertEqual(result, ControllerStatus.DOES_NOT_EXISTS)
        self.assertRaises(DoesNotExist, lambda: PropertyDoc.objects.get(id=test_id))

    def test_unauthorized_update(self):
        _price = 15
        test_id = "60999999a651cad33ea0510f"
        result = update_prop({
            "price": _price,
            "terrain_height": 2,
            "terrain_width": 3,
            "id": self._propId
        }, test_id)

        self.assertEqual(result, ControllerStatus.UNAUTHORIZED)
        self.assertNotEqual(str(PropertyDoc.objects.get(id=self._propId).owner.id), test_id)
        self.assertNotEqual(PropertyDoc.objects.get(id=self._propId).price, self._register_prop["price"])


class DeletePropertyTest(TestCase):
    _email = "test@example.net"
    _password = "testpass"
    _userId = ""
    _propId = ""
    _register_user = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": _email,
        "profile": {
            "contact_email": _email
        }
    }
    _register_prop = {
        "address": "1234 Test Street",
        "bathrooms_amount": 1.5,
        "bedrooms_amount": 3,
        "contract_type": "rent",
        "currency_code": "EUR",
        "floors_amount": 1,
        "garage_size": 2,
        "price": 120000,
        "terrain_height": 5,
        "terrain_width": 7
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._register_user).save()
        self._userId = str(new_user.id)
        new_prop = PropertyDoc(**self._register_prop, owner=self._userId).save()
        self._propId = str(new_prop.id)

    def tearDown(self) -> None:
        disconnect()

    def test_successful_delete(self):
        result = delete_prop({
            "id": self._propId
        }, self._userId)

        self.assertEqual(result, ControllerStatus.SUCCESS)
        self.assertRaises(DoesNotExist, lambda: PropertyDoc.objects.get(id=self._propId))

    def test_nonexistent_property(self):
        test_id = "60999999a651cad33ea0510f"
        result = delete_prop({
            "id": test_id
        }, self._userId)

        self.assertEqual(result, ControllerStatus.DOES_NOT_EXISTS)
        self.assertRaises(DoesNotExist, lambda: PropertyDoc.objects.get(id=test_id))

    def test_unauthorized_delete(self):
        test_id = "60999999a651cad33ea0510f"
        prop_doc = PropertyDoc.objects.get(id=self._propId)
        result = delete_prop({
            "id": self._propId
        }, test_id)

        self.assertEqual(result, ControllerStatus.UNAUTHORIZED)
        self.assertNotEqual(str(prop_doc["owner"].id), test_id)


class GetPropertyDataTest(TestCase):
    _email = "test@example.net"
    _password = "testpass"
    _userId = ""
    _propId = ""
    _register_user = {
        "username": "testuser",
        "passwd_hash": generate_password_hash(_password),
        "email": _email,
        "profile": {
            "contact_email": _email
        }
    }
    _register_prop = {
        "address": "1234 Test Street",
        "bathrooms_amount": 1.5,
        "bedrooms_amount": 3,
        "contract_type": "rent",
        "currency_code": "EUR",
        "floors_amount": 1,
        "garage_size": 2,
        "price": 120000,
        "terrain_height": 5,
        "terrain_width": 7
    }

    def setUp(self) -> None:
        connect("fast-home-test", host="mongomock://localhost")
        new_user = User(**self._register_user).save()
        self._userId = str(new_user.id)
        new_prop = PropertyDoc(**self._register_prop, owner=self._userId).save()
        self._propId = str(new_prop.id)

    def tearDown(self) -> None:
        disconnect()

    def test_successful_specific_property(self):
        result = get_property_data(self._propId)

        self.assertEqual(result[0], ControllerStatus.SUCCESS)
        self.assertEqual(result[1].address, self._register_prop["address"])

    def test_property_not_found(self):
        test_id = "60999999a651cad33ea0510f"
        result = get_property_data(test_id)

        self.assertEqual(result, (ControllerStatus.DOES_NOT_EXISTS, None))
        self.assertRaises(DoesNotExist, lambda: PropertyDoc.objects.get(id=test_id))
