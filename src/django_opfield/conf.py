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

    def _get_user_settings(
        self, setting: str | None = None, fallback: Any = None
    ) -> Any:
        user_settings = getattr(settings, OPFIELD_SETTINGS_NAME, {})
        return user_settings.get(setting, fallback)

    @property
    def OP_CLI_PATH(self) -> Path:
        if user_cli_path := self._get_user_settings("OP_CLI_PATH"):
            path = user_cli_path
        elif env_cli_path := os.environ.get("OP_CLI_PATH", None):
            path = env_cli_path
        else:
            path = shutil.which("op")

        if not path:
            raise ImportError("Could not find the 'op' CLI command")

        return Path(path).resolve()

    @property
    def OP_SERVICE_ACCOUNT_TOKEN(self) -> str:
        if user_token := self._get_user_settings("OP_SERVICE_ACCOUNT_TOKEN"):
            token = user_token
        else:
            token = os.environ.get("OP_SERVICE_ACCOUNT_TOKEN", None)

        if not token:
            raise ImproperlyConfigured("OP_SERVICE_ACCOUNT_TOKEN is not set")

        return token


app_settings = AppSettings()
