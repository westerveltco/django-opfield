from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
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
    def OP_CLI_PATH(self) -> Path:
        user_settings = getattr(settings, OPFIELD_SETTINGS_NAME, {})
        if user_cli_path := user_settings.get("OP_CLI_PATH", None):
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
        return os.environ.get("OP_SERVICE_ACCOUNT_TOKEN", "")


app_settings = AppSettings()
