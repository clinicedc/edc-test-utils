from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from edc_appointment.models import Appointment
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED


class SubjectVisitTestCaseMixin:
    @property
    def subject_visit_model_cls(self):
        return django_apps.get_model(settings.SUBJECT_VISIT_MODEL)

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(settings.SUBJECT_SCREENING_MODEL)

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(settings.SUBJECT_CONSENT_MODEL)

    def get_subject_screening(
        self, screening_identifier=None, age_in_years=None, initials=None, **kwargs
    ):
        age_in_years = age_in_years or 25
        initials = initials or "XX"
        try:
            subject_screening = self.subject_screening_model_cls.objects.get(
                screening_identifier=screening_identifier
            )
        except ObjectDoesNotExist:
            subject_screening = self.subject_screening_model_cls.objects.create(
                screening_identifier=screening_identifier,
                age_in_years=age_in_years,
                initials=initials,
                **kwargs,
            )
        except LookupError:
            subject_screening = None
        return subject_screening

    def get_subject_consent(self, subject_screening, consent_datetime=None, **kwargs):
        consent_datetime = consent_datetime or subject_screening.report_datetime
        dob = (consent_datetime or get_utcnow()).date() - relativedelta(
            years=subject_screening.age_in_years
        )
        options = dict(
            user_created="erikvw",
            user_modified="erikvw",
            dob=dob,
            site=Site.objects.get(id=settings.SITE_ID),
            consent_datetime=consent_datetime,
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
        )
        options.update(**kwargs)
        return self.subject_consent_model_cls.objects.create(**options)

    @staticmethod
    def get_appointment(**kwargs):
        return Appointment.objects.get(**kwargs)

    def get_subject_visit(
        self,
        visit_code=None,
        visit_code_sequence=None,
        subject_screening=None,
        subject_consent=None,
        reason=None,
        appointment=None,
        appt_datetime=None,
        report_datetime=None,
    ):
        reason = reason or SCHEDULED
        if not appointment:
            subject_consent = subject_consent or self.get_subject_consent(
                subject_screening or self.get_subject_screening()
            )
            options = dict(
                subject_identifier=subject_consent.subject_identifier,
                visit_code=visit_code or DAY1,
                visit_code_sequence=(
                    visit_code_sequence if visit_code_sequence is not None else 0
                ),
                reason=reason,
            )
            if appt_datetime:
                options.update(appt_datetime=appt_datetime)
            appointment = self.get_appointment(**options)
        try:
            return self.subject_visit_model_cls.objects.get(appointment=appointment)
        except ObjectDoesNotExist:
            return self.subject_visit_model_cls.objects.create(
                appointment=appointment,
                reason=reason,
                report_datetime=report_datetime or appt_datetime or appointment.appt_datetime,
            )

    def get_next_subject_visit(
        self,
        subject_visit=None,
        reason=None,
        appt_datetime=None,
        report_datetime=None,
    ):
        visit_code = (
            subject_visit.appointment.visit_code
            if reason == UNSCHEDULED
            else subject_visit.appointment.next.visit_code
        )
        # visit_code_sequence will increment in get_subject_visit
        visit_code_sequence = (
            subject_visit.appointment.visit_code_sequence if reason == UNSCHEDULED else 0
        )
        return self.get_subject_visit(
            visit_code=visit_code,
            visit_code_sequence=visit_code_sequence,
            reason=reason,
            appt_datetime=appt_datetime,
            subject_screening=self.subject_screening_model_cls.objects.get(
                subject_identifier=subject_visit.subject_identifier
            ),
            subject_consent=self.subject_consent_model_cls.objects.get(
                subject_identifier=subject_visit.subject_identifier
            ),
            report_datetime=report_datetime,
        )
