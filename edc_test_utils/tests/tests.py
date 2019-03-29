import os

from unittest.case import TestCase
from unittest import mock

from ..default_test_settings import DefaultTestSettings


class TestUtils(TestCase):
    def test_(self):

        os.environ["TRAVIS"] = ""
        base_dir = os.path.dirname(os.path.abspath(__file__))

        with mock.patch("sys.argv", ["tests.py"]):
            DEFAULT_SETTINGS = DefaultTestSettings(
                calling_file=__file__,
                BASE_DIR=base_dir,
                APP_NAME="edc_test_utils",
                ETC_DIR=os.path.join(base_dir, "etc"),
            ).settings

        self.assertIn(
            "sqlite", DEFAULT_SETTINGS.get("DATABASES").get("default").get("ENGINE")
        )

    def test_3(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.environ["TRAVIS"] = "True"
        with mock.patch("sys.argv", ["tests.py"]):
            DEFAULT_SETTINGS = DefaultTestSettings(
                calling_file="tests.py",
                BASE_DIR=base_dir,
                APP_NAME="edc_test_utils",
                ETC_DIR=os.path.join(base_dir, "etc"),
            ).settings

        self.assertIn(
            "mysql", DEFAULT_SETTINGS.get("DATABASES").get("default").get("ENGINE")
        )

    def test_encryption_keys(self):
        with mock.patch("sys.argv", ["tests.py"]):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            DEFAULT_SETTINGS = DefaultTestSettings(
                calling_file="tests.py",
                app_name="edc_test_utils",
                base_dir=base_dir,
                installed_apps=["django_crypto_fields.apps.AppConfig"],
                etc_dir=os.path.join(base_dir, "etc"),
            ).settings

        self.assertTrue(os.path.exists(DEFAULT_SETTINGS.get("KEY_PATH")))
        self.assertIn("AUTO_CREATE_KEYS", DEFAULT_SETTINGS)
