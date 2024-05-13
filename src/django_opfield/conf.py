from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

OPFIELD_SETTINGS_NAME = "DJANGO_OPFIELD"


@dataclass(frozen=True)
class AppSettings:
    def __getattr__(self, __name: str) -> Any:
        return self._get_user_settings(__name, super().__getattribute__(__name))

    def _get_user_settings(self, setting: str, fallback: Any = None) -> Any:
        user_settings = getattr(settings, OPFIELD_SETTINGS_NAME, {})

        if user_setting := user_settings.get(setting, fallback):
            ret = user_setting
        else:
            ret = os.environ.get(setting, None)

        return ret

    @property
    def OP_CLI_PATH(self) -> Path:
        if user_cli_path := self._get_user_settings("OP_CLI_PATH"):
            path = user_cli_path
        else:
            path = shutil.which("op")

        if not path:
            raise ImportError("Could not find the 'op' CLI command")

        return Path(path).resolve()

    @property
    def OP_SERVICE_ACCOUNT_TOKEN(self) -> str:
        token = self._get_user_settings("OP_SERVICE_ACCOUNT_TOKEN")

        if not token:
            raise ImproperlyConfigured("OP_SERVICE_ACCOUNT_TOKEN is not set")

        return token


app_settings = AppSettings()
