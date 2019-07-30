from django.urls.base import reverse
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist


def get_or_create_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        group = Group.objects.create(name=group_name)
    return group


def login(testcase, user=None, superuser=None, groups=None, redirect_url=None):
    user = testcase.user if user is None else user
    superuser = True if superuser is None else superuser
    if not superuser:
        user.is_superuser = False
        user.is_active = True
        user.save()
        for group_name in groups:
            group = get_or_create_group(group_name)
            user.groups.add(group)
    form = (
        testcase.app.get(reverse(redirect_url or settings.LOGIN_REDIRECT_URL))
        .maybe_follow()
        .form
    )
    form["username"] = user.username
    form["password"] = "pass"
    return form.submit()
