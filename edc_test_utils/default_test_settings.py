import sys
import os


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


class DefaultTestSettings:

    def __init__(self, calling_file=None, use_test_urls=None, add_dashboard_middleware=None,
                 template_dirs=None, **kwargs):
        self.calling_file = os.path.basename(
            calling_file) if calling_file else None
        self.base_dir = kwargs.get("BASE_DIR")
        self.app_name = kwargs.get("APP_NAME")
        self.use_test_urls = use_test_urls
        self.add_dashboard_middleware = add_dashboard_middleware
        self.kwargs = {}

        self.update_settings()
        self.post_update()
        self.kwargs.update(**kwargs)
        if template_dirs:
            self.kwargs['TEMPLATES'][0]['DIRS'] = template_dirs

    @property
    def settings(self):
        return self.kwargs

    def update_settings(self):
        """Assumes BASE_DIR, APP_NAME, INSTALLED_APPS are in kwargs.
        """

        self.kwargs.update(
            ALLOWED_HOSTS=["localhost"],
            # AUTH_USER_MODEL='custom_user.CustomUser',
            STATIC_URL="/static/",
            DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "APP_DIRS": True,
                    "OPTIONS": {
                        "context_processors": [
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
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
            EDC_BOOTSTRAP=None,
            ETC_DIR=os.path.join(self.base_dir, "etc"),
            GIT_DIR=self.base_dir,
            LIVE_SYSTEM=False,
            REVIEWER_SITE_ID=0,
            SITE_ID=40,
            DASHBOARD_URL_NAMES={
                "subject_models_url": "subject_models_url",
                "subject_listboard_url": "ambition_dashboard:subject_listboard_url",
                "screening_listboard_url": "ambition_dashboard:screening_listboard_url",
                "subject_dashboard_url": "ambition_dashboard:subject_dashboard_url",
            },
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
            EMAIL_CONTACTS={
                "data_request": "someone@example.com",
                "data_manager": "someone@example.com",
                "tmg": "someone@example.com",
            },
            EMAIL_ENABLED=True,
            TWILIO_ENABLED=False,
            DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST=None,
            DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME=None,
            DJANGO_COLLECT_OFFLINE_FILES_USER=None,
            DJANGO_COLLECT_OFFLINE_SERVER_IP=None,
            DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage",
            MIGRATION_MODULES=DisableMigrations(),
            PASSWORD_HASHERS=(
                "django.contrib.auth.hashers.MD5PasswordHasher",),
        )

    def post_update(self):

        # update settings if running runtests directly from the command line
        if self.calling_file == sys.argv[0]:
            key_path = os.path.join(self.base_dir, "etc")
            if not os.path.exists(key_path):
                os.mkdir(key_path)
            self.kwargs.update(DEBUG=False, KEY_PATH=key_path,
                               AUTO_CREATE_KEYS=False)
            if len(os.listdir(key_path)) == 0:
                self.kwargs.update(AUTO_CREATE_KEYS=True)

        if os.environ.get("TRAVIS"):
            self.kwargs.update(
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

        if self.use_test_urls:
            self.kwargs.update(ROOT_URLCONF=f"{self.app_name}.tests.urls")
        else:
            self.kwargs.update(ROOT_URLCONF=f"{self.app_name}.urls")

        if self.add_dashboard_middleware:
            self.kwargs["MIDDLEWARE"].extend(
                [
                    "edc_dashboard.middleware.DashboardMiddleware",
                    "edc_subject_dashboard.middleware.DashboardMiddleware",
                ]
            )
