from django.apps import apps as django_apps
from edc_list_data.model_mixins import ListModelMixin
from unittest.case import TestCase


class NaturalKeyTestHelperError(Exception):
    pass


class NaturalKeyTestHelper(TestCase):
    def nk_test_natural_key_attr(self, *app_labels, exclude_models=None):

        """Asserts all models in given apps have a
        natural_key model method.
        """
        exclude_models = exclude_models or []
        for app_label in app_labels:
            models = django_apps.get_app_config(app_label).get_models()
            for model in models:
                if (
                    model._meta.label_lower not in exclude_models
                    and not issubclass(model, ListModelMixin)
                    and ".tests." not in model.__module__
                ):
                    self.assertTrue(
                        "natural_key" in dir(model),
                        "Model method 'natural_key' missing. "
                        f"Got '{model._meta.label_lower}'.",
                    )

    def nk_test_get_by_natural_key_attr(self, *app_labels, exclude_models=None):
        """Asserts all models in given apps have a get_by_natural_key
        manager method.
        """
        exclude_models = exclude_models or []
        for app_label in app_labels:
            models = django_apps.get_app_config(app_label).get_models()
            for model in models:
                if (
                    model._meta.label_lower not in exclude_models
                    and not issubclass(model, ListModelMixin)
                    and ".tests." not in model.__module__
                ):
                    self.assertTrue(
                        "get_by_natural_key" in dir(model.objects),
                        "Manager method 'get_by_natural_key' missing. "
                        f"Got '{model._meta.label_lower}'.",
                    )

    def nk_test_natural_keys(self, complete_required_crfs):
        """Asserts tuple from natural_key when passed to
        get_by_natural_key successfully gets the model instance.
        """
        for objs in complete_required_crfs.values():
            for obj in objs:
                options = obj.natural_key()
                try:
                    obj.__class__.objects.get_by_natural_key(*options)
                except obj.__class__.DoesNotExist:
                    self.fail(
                        "get_by_natural_key query failed for "
                        f"'{obj._meta.label_lower}' with "
                        f"options {options}."
                    )
                except TypeError as e:
                    raise NaturalKeyTestHelperError(
                        f"{e} See {obj._meta.label_lower}. Got {options}."
                    )

    def nk_test_natural_key_by_schedule(self, visits=None, visit_attr=None):
        """A wrapper method for natural_keys that use
        the enrollment instance to test each CRF in each visit
        in the schedule linked to the enrollment model.
        """
        complete_required_crfs = {}
        for visit in visits:
            complete_required_crfs.update(
                {
                    visit.visit_code: self.complete_required_crfs(
                        visit_code=visit.visit_code,
                        visit=visit,
                        visit_attr=visit_attr,
                        subject_identifier=visit.subject_identifier,
                    )
                }
            )
        self.nk_test_natural_keys(complete_required_crfs)
