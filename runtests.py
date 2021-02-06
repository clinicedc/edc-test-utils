#!/usr/bin/env python
import logging
import os
import sys
from os.path import abspath, dirname

import arrow
import django
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.test.runner import DiscoverRunner

from edc_test_utils import DefaultTestSettings

app_name = "edc_test_utils"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    ADVERSE_EVENT_APP_LABEL="adverse_event_app",
    ADVERSE_EVENT_ADMIN_SITE="adverse_event_app_admin",
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=arrow.utcnow().floor("hour") - relativedelta(years=2),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=arrow.utcnow().ceil("hour") + relativedelta(years=2),
    EDC_NAVBAR_DEFAULT=app_name,
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
    ],
    add_dashboard_middleware=True,
    use_test_urls=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests([f"{app_name}.tests"])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
