from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any

from django.conf import settings

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import (
        override,  # pyright: ignore[reportUnreachable]  # pragma: no cover
    )

OPFIELD_SETTINGS_NAME = "DJANGO_OPFIELD"


@dataclass(frozen=True)
class AppSettings:
    @override
    def __getattribute__(self, __name: str) -> Any:
        user_settings = getattr(settings, OPFIELD_SETTINGS_NAME, {})
        return user_settings.get(__name, super().__getattribute__(__name))

    @property
    def OP_SERVICE_ACCOUNT_TOKEN(self) -> str:
        return os.environ.get("OP_SERVICE_ACCOUNT_TOKEN", "")


app_settings = AppSettings()
