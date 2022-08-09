import string
from datetime import date, datetime
from random import choice

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from edc_consent.site_consents import site_consents
from edc_constants.constants import FEMALE, MALE
from edc_utils import get_utcnow
from faker.providers import BaseProvider


class EdcBaseProvider(BaseProvider):
    @property
    def consent_model(self):
        return django_apps.get_app_config("edc_base_test").consent_model

    @staticmethod
    def gender() -> str:
        return choice([FEMALE, MALE])  # nosec B311

    @staticmethod
    def initials() -> str:
        return choice(list(string.ascii_uppercase)) + choice(  # nosec B311
            list(string.ascii_uppercase)
        )

    def dob_for_consenting_adult(self) -> date:
        consent = site_consents.get_consent(
            consent_model=self.consent_model, report_datetime=get_utcnow()
        )
        years = choice(range(consent.age_is_adult, consent.age_max + 1))  # nosec B311
        return (get_utcnow() - relativedelta(years=years)).date()

    def dob_for_consenting_minor(self) -> date:
        consent = site_consents.get_consent(self.consent_model, report_datetime=get_utcnow())
        years = consent.age_min - 1
        return (get_utcnow() - relativedelta(years=years)).date()

    def age_for_consenting_adult(self) -> int:
        consent = site_consents.get_consent(
            consent_model=self.consent_model, report_datetime=get_utcnow()
        )
        return choice(range(consent.age_is_adult, consent.age_max + 1))  # nosec B311

    def age_for_consenting_minor(self) -> int:
        consent = site_consents.get_consent(
            consent_model=self.consent_model, report_datetime=get_utcnow()
        )
        return choice(range(consent.age_min, consent.age_is_adult + 1))  # nosec B311

    @staticmethod
    def yesterday() -> datetime:
        return get_utcnow() - relativedelta(days=1)

    @staticmethod
    def last_week() -> datetime:
        return get_utcnow() - relativedelta(weeks=1)

    @staticmethod
    def last_month() -> datetime:
        return get_utcnow() - relativedelta(months=1)

    @staticmethod
    def two_months_ago() -> datetime:
        return get_utcnow() - relativedelta(months=2)

    @staticmethod
    def three_months_ago() -> datetime:
        return get_utcnow() - relativedelta(months=3)

    @staticmethod
    def six_months_ago() -> datetime:
        return get_utcnow() - relativedelta(months=6)

    @staticmethod
    def twelve_months_ago() -> datetime:
        return get_utcnow() - relativedelta(months=12)
