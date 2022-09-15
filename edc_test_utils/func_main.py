from __future__ import annotations

import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


def func_main(project_settings, *project_tests):
    if not settings.configured:
        settings.configure(**project_settings)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failfast = any([True for t in sys.argv if t.startswith("--failfast")])
    failures = DiscoverRunner(failfast=failfast, tags=tags).run_tests(project_tests)
    sys.exit(failures)
