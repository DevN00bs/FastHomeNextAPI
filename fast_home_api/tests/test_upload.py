from os.path import join, dirname
from unittest import TestCase

from werkzeug.datastructures import FileStorage, Headers

import fast_home_api.controllers.upload as upl
from fast_home_api.utils.enums import ControllerStatus


class CheckFileTypeTests(TestCase):
    _image: FileStorage
    _non_image: FileStorage

    def setUp(self) -> None:
        self._image = FileStorage(open(join(dirname(__file__), "../templates/img/logo.png"), "rb"),
                                  headers=Headers({"Content-Type": "image/png"}))
        self._non_image = FileStorage(open(join(dirname(__file__), "../templates/verify.html")),
                                      headers=Headers({"Content-Type": "text/html"}))

    def tearDown(self) -> None:
        self._image.close()
        self._non_image.close()

    def test_file_is_image(self):
        result = upl.check_file_type([self._image])

        self.assertEqual(result, ControllerStatus.SUCCESS)
        self.assertEqual(self._image.mimetype, "image/png")

    def test_file_is_not_image(self):
        result = upl.check_file_type([self._non_image])

        self.assertEqual(result, ControllerStatus.NOT_AN_IMAGE)
        self.assertEqual(self._non_image.mimetype, "text/html")
