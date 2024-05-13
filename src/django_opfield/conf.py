from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import (
        override,  # pyright: ignore[reportUnreachable]  # pragma: no cover
    )

OPFIELD_SETTINGS_NAME = "DJANGO_OPFIELD"


def _get_user_setting(setting: str, fallback: Any = None) -> Any:
    user_settings = getattr(settings, OPFIELD_SETTINGS_NAME, {})

    if user_setting := user_settings.get(setting, fallback):
        ret = user_setting
    else:
        ret = os.environ.get(setting, None)

    return ret


@dataclass(frozen=True)
class AppSettings:
    OP_COMMAND_TIMEOUT: int = 5  # in seconds
    OP_CLI_PATH: str = ""
    OP_SERVICE_ACCOUNT_TOKEN: str = ""

    @override
    def __getattribute__(self, __name: str) -> Any:
        user_setting = _get_user_setting(__name)
        return user_setting or super().__getattribute__(__name)

    def get_op_cli_path(self) -> Path:
        path: str | None = None

        if user_cli_path := self.OP_CLI_PATH:
            path = user_cli_path
        else:
            path = shutil.which("op")

        if not path:
            raise ImportError("Could not find the 'op' CLI command")

        return Path(path).resolve()

    def get_op_service_account_token(self) -> str:
        token = self.OP_SERVICE_ACCOUNT_TOKEN

        if not token:
            raise ImproperlyConfigured("OP_SERVICE_ACCOUNT_TOKEN is not set")

        return token


app_settings = AppSettings()
