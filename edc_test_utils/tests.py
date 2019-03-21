import os

from unittest.case import TestCase
from unittest import mock

from .default_test_settings import DefaultTestSettings


class TestUtils(TestCase):
    def test_(self):

        os.environ["TRAVIS"] = ""
        base_dir = os.path.dirname(os.path.abspath(__file__))

        DEFAULT_SETTINGS = DefaultTestSettings(BASE_DIR=base_dir).settings

        self.assertIn(
            "sqlite", DEFAULT_SETTINGS.get(
                "DATABASES").get("default").get("ENGINE")
        )

    def test_2(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        with mock.patch("sys.argv", ["tests.py"]):
            DEFAULT_SETTINGS = DefaultTestSettings(
                BASE_DIR=base_dir, calling_file=__file__
            ).settings

        self.assertFalse(DEFAULT_SETTINGS.get("DEBUG"))
        self.assertEqual(
            DEFAULT_SETTINGS.get("KEY_PATH"), os.path.join(base_dir, "etc")
        )
        self.assertIn("AUTO_CREATE_KEYS", DEFAULT_SETTINGS)

    def test_3(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ["TRAVIS"] = "True"
        DEFAULT_SETTINGS = DefaultTestSettings(BASE_DIR=base_dir).settings

        self.assertIn(
            "mysql", DEFAULT_SETTINGS.get(
                "DATABASES").get("default").get("ENGINE")
        )
