import sys
import os


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


def default_test_settings(default_settings=None, base_dir=None, calling_file=None):

    print(sys.argv)
    print(calling_file)
    if calling_file:
        calling_file = os.path.basename(calling_file)

    default_settings.update(
        BASE_DIR=base_dir,
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
        ],
        LANGUAGE_CODE="en-us",
        TIME_ZONE="UTC",
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage",
        MIGRATION_MODULES=DisableMigrations(),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        ETC_DIR=os.path.join(base_dir, "etc"),
        COUNTRY="botswana",
        DASHBOARD_URL_NAMES={
            "subject_models_url": "subject_models_url",
            "subject_listboard_url": "ambition_dashboard:subject_listboard_url",
            "screening_listboard_url": "ambition_dashboard:screening_listboard_url",
            "subject_dashboard_url": "ambition_dashboard:subject_dashboard_url",
        },
        EDC_BOOTSTRAP=3,
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        EMAIL_CONTACTS={
            "data_request": "someone@example.com",
            "data_manager": "someone@example.com",
            "tmg": "someone@example.com",
        },
        EMAIL_ENABLED=True,
        GIT_DIR=base_dir,
        LIVE_SYSTEM=False,
        REVIEWER_SITE_ID=0,
        SITE_ID=40,
        TWILIO_ENABLED=False,
        DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST=None,
        DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME=None,
        DJANGO_COLLECT_OFFLINE_FILES_USER=None,
        DJANGO_COLLECT_OFFLINE_SERVER_IP=None,
    )

    # update settings if running runtests directly from the command line
    if calling_file == sys.argv[0]:
        key_path = os.path.join(base_dir, "etc")
        if not os.path.exists(key_path):
            os.mkdir(key_path)
        default_settings.update(DEBUG=False, KEY_PATH=key_path, AUTO_CREATE_KEYS=False)
        if len(os.listdir(key_path)) == 0:
            default_settings.update(AUTO_CREATE_KEYS=True)

    if os.environ.get("TRAVIS"):
        default_settings.update(
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

    return default_settings
