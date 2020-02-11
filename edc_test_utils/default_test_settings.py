import sys
import os


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


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
        template_dirs=None,
        installed_apps=None,
        **kwargs,
    ):

        self.calling_file = os.path.basename(calling_file) if calling_file else None
        self.base_dir = base_dir or kwargs.get("BASE_DIR")
        self.app_name = app_name or kwargs.get("APP_NAME")
        self.installed_apps = installed_apps or kwargs.get("INSTALLED_APPS")
        self.etc_dir = etc_dir or kwargs.get("ETC_DIR")

        self.settings = dict(
            APP_NAME=self.app_name,
            BASE_DIR=self.base_dir,
            INSTALLED_APPS=self.installed_apps or [],
            ETC_DIR=self.etc_dir,
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
        if "django_crypto_fields.apps.AppConfig" in self.settings.get("INSTALLED_APPS"):
            self._manage_encryption_keys()
        self.check_travis()

    def update_root_urlconf(self, use_test_urls=None):
        if "ROOT_URLCONF" not in self.settings:
            if use_test_urls:
                self.settings.update(ROOT_URLCONF=f"{self.app_name}.tests.urls")
            else:
                self.settings.update(ROOT_URLCONF=f"{self.app_name}.urls")

    def _update_defaults(self):
        """Assumes BASE_DIR, APP_NAME, INSTALLED_APPS are in kwargs.
        """

        self.settings.update(
            ALLOWED_HOSTS=["localhost"],
            # AUTH_USER_MODEL='custom_user.CustomUser',
            STATIC_URL="/static/",
            DATABASES={
                # required for tests when acting as a server that deserializes
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": os.path.join(self.base_dir, "db.sqlite3"),
                }
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
            COUNTRY="botswana",
            EDC_BOOTSTRAP=3,
            GIT_DIR=self.base_dir,
            LIVE_SYSTEM=False,
            REVIEWER_SITE_ID=0,
            SITE_ID=40,
            USE_EDC_FACILITY_DEFAULTS=True,
            HOLIDAY_FILE=os.path.join(
                self.base_dir, self.app_name, "tests", "holidays.csv"
            ),
            DASHBOARD_URL_NAMES={},
            DASHBOARD_BASE_TEMPLATES={},
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
            EMAIL_CONTACTS={
                "data_request": "someone@example.com",
                "data_manager": "someone@example.com",
                "tmg": "someone@example.com",
            },
            EMAIL_ENABLED=True,
            TWILIO_ENABLED=False,
            TWILIO_TEST_RECIPIENT="+15555555555",
            SUBJECT_CONSENT_MODEL=f"{self.app_name}.subjectconsent",
            SUBJECT_VISIT_MODEL=f"{self.app_name}.subjectvisit",
            SUBJECT_REQUISITION_MODEL=f"{self.app_name}.subjectrequisition",
            ADVERSE_EVENT_ADMIN_SITE="adverse_event_app_admin",
            ADVERSE_EVENT_APP_LABEL="adverse_event_app",
            DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST=None,
            DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME=None,
            DJANGO_COLLECT_OFFLINE_FILES_USER=None,
            DJANGO_COLLECT_OFFLINE_SERVER_IP=None,
            EDC_RANDOMIZATION_LIST_MODEL="edc_randomization.randomizationlist",
            EDC_RANDOMIZATION_LIST_PATH=self.etc_dir,
            DATA_DICTIONARY_APP_LABELS=[],
            DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage",
            MIGRATION_MODULES=DisableMigrations(),
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
