from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from edc_sites.site import SiteNotRegistered, sites
from edc_sites.utils import get_site_model_cls

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def get_user_for_tests(
    username: str | None = None,
    codenames: list[tuple[str, str]] | None = None,
    view_only: bool | None = None,
    is_superuser: bool | None = None,
) -> User:
    """Returns a User model instance ready for tests.

    Adds:
        - user permissions to something (default is Appointment)
        - a site to the user's userprofile

    `edc_sites` and `edc_auth` are a required apps
    for INSTALLED_APPS in runtests.

    Tests against edc dashboard like Views need the
    user to have permissions.
    """
    user = get_user_model().objects.create_superuser(
        username or "user_login", "u@example.com", "pass"
    )
    user.is_active = True
    user.is_staff = True
    user.is_superuser = False if is_superuser is None else is_superuser
    user.save()
    user.refresh_from_db()

    # at least on site should be registered. You can
    #  - use settings.EDC_SITES_REGISTER_DEFAULT=True
    #  - manually register in the test or test setup.
    #  - austodiscover sites.py in your app or test_app
    if not sites.all():
        raise SiteNotRegistered(
            "Failed to create test user. Cannot update userprofile.sites. "
            "No sites have been registered!"
        )
    # will raise an exception if edc_auth not installed
    user.userprofile.sites.add(get_site_model_cls().objects.get_current())

    if codenames is None:
        codenames = [
            ("edc_appointment", "view_appointment"),
            ("edc_appointment", "add_appointment"),
            ("edc_appointment", "change_appointment"),
        ]
    for app_label, codename in codenames:
        if view_only and not codename.startswith("view_"):
            continue
        user.user_permissions.add(
            Permission.objects.get(codename=codename, content_type__app_label=app_label)
        )
    return user
