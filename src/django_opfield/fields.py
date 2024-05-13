from __future__ import annotations

import subprocess
import sys
from typing import Any

from django.db import models

from django_opfield.conf import app_settings
from django_opfield.validators import OPURIValidator

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import (
        override,  # pyright: ignore[reportUnreachable]  # pragma: no cover
    )


class OPField(models.CharField):
    description = "1Password secret"

    def __init__(
        self,
        vaults: list[str] | None = None,
        secret_name: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.vaults = vaults
        self.secret_name = secret_name
        kwargs.setdefault("max_length", 255)
        super().__init__(*args, **kwargs)
        self.validators.append(OPURIValidator(vaults=self.vaults))

    @override
    def contribute_to_class(
        self, cls: type[models.Model], name: str, private_only: bool = False
    ):
        super().contribute_to_class(cls, name, private_only)

        def get_secret(self: models.Model) -> str | None:
            op = app_settings.get_op_cli_path()
            op_uri = getattr(self, name)
            op_token = app_settings.get_op_service_account_token()
            op_timeout = app_settings.OP_COMMAND_TIMEOUT
            result = subprocess.run(
                [op, "read", op_uri],
                capture_output=True,
                env={"OP_SERVICE_ACCOUNT_TOKEN": op_token},
                timeout=op_timeout,
            )
            if result.returncode != 0:
                raise ValueError(
                    f"Could not read secret from 1Password: {result.stderr.decode('utf-8')}"
                )
            return result.stdout.decode("utf-8").strip()

        def set_secret(self: models.Model, value: str) -> None:
            raise NotImplementedError("OPField does not support setting secret value")

        property_name = (
            f"{name}_secret" if self.secret_name is None else self.secret_name
        )

        setattr(cls, property_name, property(get_secret, set_secret))

    @override
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.vaults is not None:
            kwargs["vaults"] = self.vaults
        return name, path, args, kwargs
