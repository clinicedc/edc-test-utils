from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from edc_sites.utils import get_site_model_cls

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def get_user_for_tests(username: str | None = None) -> User:
    user = get_user_model().objects.create_superuser(
        username or "user_login", "u@example.com", "pass"
    )
    user.is_active = True
    user.is_staff = True
    user.save()
    user.refresh_from_db()
    user.userprofile.sites.add(get_site_model_cls().objects.get(id=settings.SITE_ID))
    user.user_permissions.add(
        Permission.objects.get(
            codename="view_appointment", content_type__app_label="edc_appointment"
        )
    )
    return user
