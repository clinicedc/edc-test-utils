import secrets
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    # from edc_consent.model_mixins import ConsentModelMixin
    from edc_randomization.models import RandomizationList


def scramble_randomization_for_test_data(
    arms: list[str],
    randomization_list_model_cls: Type[RandomizationList],
    # consent_model_cls: Type[ConsentModelMixin],
):
    choices = []
    for i in range(0, 8):
        choices.append(secrets.choice(arms))
    for obj in randomization_list_model_cls.objects.all():
        obj.assigment = secrets.choice(choices)
        obj.save_base(update_fields=["assignment"])
