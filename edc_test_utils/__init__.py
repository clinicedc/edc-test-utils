from warnings import warn

from .default_test_settings import DefaultTestSettings
from .func_main import func_main

warn(
    "This path is deprecated in favor of edc_test_settings",
    DeprecationWarning,
    stacklevel=2,
)
