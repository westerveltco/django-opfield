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
    OP_CLI_PATH: str | None = None

    @override
    def __getattribute__(self, __name: str) -> Any:
        user_settings = getattr(settings, OPFIELD_SETTINGS_NAME, {})
        return user_settings.get(__name, super().__getattribute__(__name))

    def get_op_cli_path(self) -> Path:
        if self.OP_CLI_PATH is not None:
            path = self.OP_CLI_PATH
        elif env_cli_path := os.environ.get("OP_CLI_PATH", None):
            path = env_cli_path
        else:
            path = shutil.which("op")

        if not path:
            raise ImportError("Could not find the 'op' CLI command")

        return Path(path)

    @property
    def OP_SERVICE_ACCOUNT_TOKEN(self) -> str:
        return os.environ.get("OP_SERVICE_ACCOUNT_TOKEN", "")


app_settings = AppSettings()
