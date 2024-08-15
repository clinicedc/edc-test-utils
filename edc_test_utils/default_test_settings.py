from __future__ import annotations

from warnings import warn

from edc_test_settings.default_test_settings import DefaultTestSettings as NewClass


def DefaultTestSettings(*args, **kwargs):  # noqa
    warn(
        "This path is deprecated in favor of edc_test_settings.DefaultTestSettings",
        DeprecationWarning,
        stacklevel=2,
    )
    return NewClass(*args, **kwargs)
