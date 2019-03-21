# import sys
import os

from unittest.case import TestCase
from unittest import mock

from .default_test_settings import default_test_settings


class TestUtils(TestCase):
    def test_(self):
        DEFAULT_SETTINGS = {}

        os.environ["TRAVIS"] = ""
        base_dir = os.path.dirname(os.path.abspath(__file__))

        default_test_settings(
            default_settings=DEFAULT_SETTINGS, base_dir=base_dir)

        self.assertIn(
            "sqlite", DEFAULT_SETTINGS.get(
                "DATABASES").get("default").get("ENGINE")
        )

    def test_2(self):
        DEFAULT_SETTINGS = {}
        base_dir = os.path.dirname(os.path.abspath(__file__))

        with mock.patch("sys.argv", ["tests.py"]):
            default_test_settings(
                default_settings=DEFAULT_SETTINGS,
                base_dir=base_dir,
                calling_file=__file__,
            )

        self.assertFalse(DEFAULT_SETTINGS.get("DEBUG"))
        self.assertEqual(
            DEFAULT_SETTINGS.get("KEY_PATH"), os.path.join(base_dir, "etc")
        )
        self.assertIn("AUTO_CREATE_KEYS", DEFAULT_SETTINGS)

    def test_3(self):
        DEFAULT_SETTINGS = {}
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ["TRAVIS"] = "True"
        default_test_settings(
            default_settings=DEFAULT_SETTINGS, base_dir=base_dir)

        self.assertIn(
            "mysql", DEFAULT_SETTINGS.get(
                "DATABASES").get("default").get("ENGINE")
        )
