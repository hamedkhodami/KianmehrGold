from os import getenv

from .base import *

PRODUCTION = int(getenv("PRODUCTION", 0))

if PRODUCTION:
    from .production import *
else:
    from .development import *  # type: ignore
