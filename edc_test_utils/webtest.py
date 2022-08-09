from warnings import warn

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.color import color_style
from django.urls.base import reverse
from edc_auth.models import Role

style = color_style()


def get_or_create_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        group = Group.objects.create(name=group_name)
    return group


def login(
    testcase,
    user=None,
    superuser=None,
    groups=None,
    roles=None,
    sites=None,
    redirect_url=None,
):
    user = testcase.user if user is None else user
    user.is_superuser = True if superuser is None else superuser
    if user.is_superuser:
        warn(
            style.WARNING(
                "\nWarning: Running test where logged in user is a superuser. See login() \n"
            )
        )
    user.is_active = True
    user.is_staff = True
    if not user.is_superuser:
        if groups:
            user.groups.clear()
        for group_name in groups or []:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        if roles:
            user.userprofile.roles.clear()
        for role_name in roles or []:
            role = Role.objects.get(name=role_name)
            user.userprofile.roles.add(role)
        for site in Site.objects.filter(id__in=sites or [settings.SITE_ID]):
            user.userprofile.sites.add(site)
    user.userprofile.save()
    user.save()
    user.refresh_from_db()
    form = (
        testcase.app.get(reverse(redirect_url or settings.LOGIN_REDIRECT_URL))
        .maybe_follow()
        .form
    )
    form["username"] = user.username
    form["password"] = "pass"  # nosec B105
    return form.submit()
