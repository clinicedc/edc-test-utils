from __future__ import annotations

from warnings import warn

from edc_test_settings.func_main import func_main as new_func_main


def func_main(project_settings, *project_tests):
    warn(
        "This path is deprecated in favor of edc_test_settings.func_main2",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_func_main(project_settings, *project_tests)
