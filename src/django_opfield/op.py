from __future__ import annotations

import subprocess
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from django_opfield.conf import app_settings


@dataclass
class OPCli:
    op: Path = field(default_factory=app_settings.get_op_cli_path)
    command_timeout: int = field(
        default_factory=lambda: app_settings.OP_COMMAND_TIMEOUT
    )

    def __post_init__(self) -> None:
        assert app_settings.get_op_service_account_token()

    def read(self, op_uri: str) -> str:
        result = subprocess.run(
            [self.op, "read", op_uri], capture_output=True, timeout=self.command_timeout
        )
        if result.returncode != 0:
            raise ValueError(
                f"Could not read secret from 1Password: {result.stderr.decode('utf-8')}"
            )
        return result.stdout.decode("utf-8").strip()
