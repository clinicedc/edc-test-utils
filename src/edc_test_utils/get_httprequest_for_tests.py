from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sites.models import Site
from django.http import HttpRequest

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def get_request_object_for_tests(user: User) -> HttpRequest:
    request = HttpRequest()
    setattr(request, "session", "session")
    messages = FallbackStorage(request)
    setattr(request, "_messages", messages)
    setattr(request, "user", user)
    setattr(request, "site", Site.objects.get(id=settings.SITE_ID))
    return request
