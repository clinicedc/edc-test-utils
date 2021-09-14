from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.urls.base import reverse
from edc_auth.models import Role


def get_or_create_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        group = Group.objects.create(name=group_name)
    return group


def login(testcase, user=None, superuser=None, groups=None, roles=None, redirect_url=None):
    user = testcase.user if user is None else user
    user.is_superuser = True if superuser is None else superuser
    user.is_active = True
    user.is_staff = True
    if not user.is_superuser:
        for group_name in groups or []:
            group = get_or_create_group(group_name)
            user.groups.add(group)
        for role_name in roles or []:
            role = Role.objects.get(name=role_name)
            user.userprofile.roles.add(role)
    user.save()
    user.refresh_from_db()
    form = (
        testcase.app.get(reverse(redirect_url or settings.LOGIN_REDIRECT_URL))
        .maybe_follow()
        .form
    )
    form["username"] = user.username
    form["password"] = "pass"
    return form.submit()
