import os
import sys
from uuid import uuid4

import arrow
from dateutil.relativedelta import relativedelta
from django import VERSION

from .default_installed_apps import DEFAULT_EDC_INSTALLED_APPS

try:
    from multisite import SiteID
except ModuleNotFoundError:
    SiteID = None


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


def get_migrations_module():
    if VERSION <= (1, 9):
        return {
            "auth": None,
            "contenttypes": None,
            "default": None,
            "sessions": None,
            "core": None,
            "profiles": None,
            "snippets": None,
            "scaffold_templates": None,
        }
    else:
        return DisableMigrations()


class DefaultTestSettings:
    def __init__(
        self,
        base_dir=None,
        app_name=None,
        calling_file=None,
        etc_dir=None,
        use_test_urls=None,
        add_dashboard_middleware=None,
        add_lab_dashboard_middleware=None,
        add_adverse_event_dashboard_middleware=None,
        template_dirs=None,
        excluded_apps=None,
        **kwargs,
    ):

        self.calling_file = os.path.basename(calling_file) if calling_file else None
        self.base_dir = base_dir or kwargs.get("BASE_DIR")
        self.app_name = app_name or kwargs.get("APP_NAME")
        self.installed_apps = [
            app
            for app in (kwargs.get("INSTALLED_APPS") or DEFAULT_EDC_INSTALLED_APPS)
            if app not in (excluded_apps or [])
        ]
        self.etc_dir = (
            etc_dir
            or kwargs.get("ETC_DIR")
            or os.path.join(self.base_dir, self.app_name, "tests", "etc")
        )
        self.settings = dict(
            APP_NAME=self.app_name,
            BASE_DIR=self.base_dir,
            INSTALLED_APPS=self.installed_apps,
            ETC_DIR=(
                self.etc_dir or os.path.join(self.base_dir, self.app_name, "tests", "etc")
            ),
            TEST_DIR=os.path.join(self.base_dir, self.app_name, "tests"),
        )

        self._update_defaults()
        # override / add from params
        self.settings.update(**kwargs)

        if template_dirs:
            self.settings["TEMPLATES"][0]["DIRS"] = template_dirs

        self.update_root_urlconf(use_test_urls)

        if add_dashboard_middleware:
            self.settings["MIDDLEWARE"].extend(
                [
                    "edc_dashboard.middleware.DashboardMiddleware",
                    "edc_subject_dashboard.middleware.DashboardMiddleware",
                ]
            )

        if add_lab_dashboard_middleware:
            self.settings["MIDDLEWARE"].extend(
                ["edc_lab_dashboard.middleware.DashboardMiddleware"]
            )
        if add_adverse_event_dashboard_middleware:
            self.settings["MIDDLEWARE"].extend(
                ["edc_adverse_event.middleware.DashboardMiddleware"]
            )

        if "django_crypto_fields.apps.AppConfig" in self.installed_apps:
            self._manage_encryption_keys()
        self.check_travis()

    def update_root_urlconf(self, use_test_urls=None):
        if "ROOT_URLCONF" not in self.settings:
            if use_test_urls:
                self.settings.update(ROOT_URLCONF=f"{self.app_name}.tests.urls")
            else:
                self.settings.update(ROOT_URLCONF=f"{self.app_name}.urls")

    def _update_defaults(self):
        """Assumes BASE_DIR, APP_NAME are in kwargs."""

        self.settings.update(
            ALLOWED_HOSTS=["localhost"],
            # AUTH_USER_MODEL='custom_user.CustomUser',
            STATIC_URL="/static/",
            DATABASES={
                # required for tests when acting as a server that deserializes
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": os.path.join(self.base_dir, "db.sqlite3"),
                },
                "client": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": os.path.join(self.base_dir, "db.sqlite3"),
                },
            },
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                            "django.template.context_processors.request",
                        ]
                    },
                }
            ],
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
                "django.contrib.sites.middleware.CurrentSiteMiddleware",
            ],
            LANGUAGE_CODE="en-us",
            TIME_ZONE="UTC",
            USE_I18N=True,
            USE_L10N=True,
            USE_TZ=True,
            EDC_BOOTSTRAP=3,
            GIT_DIR=self.base_dir,
            LIVE_SYSTEM=False,
            REVIEWER_SITE_ID=0,
            SITE_ID=SiteID(default=1) if SiteID else 1,
            SECRET_KEY=uuid4().hex,
            HOLIDAY_FILE=os.path.join(self.base_dir, self.app_name, "tests", "holidays.csv"),
            INDEX_PAGE_LABEL="",
            DASHBOARD_URL_NAMES={},
            DASHBOARD_BASE_TEMPLATES={},
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
            EMAIL_CONTACTS={
                "data_request": "someone@example.com",
                "data_manager": "someone@example.com",
                "tmg": "someone@example.com",
            },
            EMAIL_ENABLED=True,
            INDEX_PAGE="http://localhost:8000",
            SENTRY_ENABLED=False,
            TWILIO_ENABLED=False,
            TWILIO_TEST_RECIPIENT="+15555555555",
            SUBJECT_SCREENING_MODEL=f"{self.app_name}.subjectscreening",
            SUBJECT_CONSENT_MODEL=f"{self.app_name}.subjectconsent",
            SUBJECT_VISIT_MODEL=f"{self.app_name}.subjectvisit",
            SUBJECT_VISIT_MISSED_MODEL=f"{self.app_name}.subjectvisitmissed",
            SUBJECT_REQUISITION_MODEL=f"{self.app_name}.subjectrequisition",
            SUBJECT_APP_LABEL=f"{self.app_name}",
            ADVERSE_EVENT_ADMIN_SITE="adverse_event_app_admin",
            ADVERSE_EVENT_APP_LABEL="adverse_event_app",
            DJANGO_COLLECT_OFFLINE_ENABLED=False,
            DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST=None,
            DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME=None,
            DJANGO_COLLECT_OFFLINE_FILES_USER=None,
            DJANGO_COLLECT_OFFLINE_SERVER_IP=None,
            EDC_NAVBAR_DEFAULT=self.app_name,
            EDC_PROTOCOL_STUDY_OPEN_DATETIME=arrow.utcnow().datetime - relativedelta(years=1),
            EDC_PROTOCOL_STUDY_CLOSE_DATETIME=arrow.utcnow().datetime + relativedelta(years=1),
            EDC_PROTOCOL_NUMBER="101",
            EDC_FACILITY_USE_DEFAULTS=True,
            EDC_FACILITY_DEFAULT_FACILITY_NAME="7-day-clinic",
            LIST_MODEL_APP_LABEL=self.app_name.replace("edc", "lists"),
            EDC_RANDOMIZATION_LIST_PATH=os.path.join(
                self.base_dir, self.app_name, "tests", "etc"
            ),
            EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=True,
            EDC_RANDOMIZATION_SKIP_VERIFY_CHECKS=True,
            EDC_SITES_MODULE_NAME=None,
            DATA_DICTIONARY_APP_LABELS=[],
            DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage",
            MIGRATION_MODULES=get_migrations_module(),
            PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        )

    def _manage_encryption_keys(self):
        # update settings if running runtests directly from the command line
        if self.calling_file and self.calling_file == sys.argv[0]:
            key_path = self.settings.get("ETC_DIR")
            if not os.path.exists(key_path):
                os.mkdir(key_path)
            auto_create_keys = True if len(os.listdir(key_path)) == 0 else False
            self.settings.update(
                DEBUG=False, KEY_PATH=key_path, AUTO_CREATE_KEYS=auto_create_keys
            )

    def check_travis(self):
        if os.environ.get("TRAVIS"):
            self.settings.update(
                DATABASES={
                    "default": {
                        "ENGINE": "django.db.backends.mysql",
                        "NAME": "edc",
                        "USER": "travis",
                        "PASSWORD": "",
                        "HOST": "localhost",
                        "PORT": "",
                    }
                }
            )
