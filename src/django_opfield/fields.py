from __future__ import annotations

import shutil
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
        self, vaults: list[str] | None = None, *args: Any, **kwargs: Any
    ) -> None:
        self.vaults = vaults
        kwargs.setdefault("max_length", 255)
        super().__init__(*args, **kwargs)
        self.validators.append(OPURIValidator(vaults=self.vaults))

    @classmethod
    def with_secret(cls, *args: Any, **kwargs: Any) -> tuple[OPField, property]:
        op_uri = cls(*args, **kwargs)

        def secret_getter(self: models.Model) -> str | None:
            if not app_settings.OP_SERVICE_ACCOUNT_TOKEN:
                msg = "OP_SERVICE_ACCOUNT_TOKEN is not set"
                raise ValueError(msg)
            if shutil.which("op") is None:
                msg = "The 'op' CLI command is not available"
                raise OSError(msg)
            field_value = getattr(self, op_uri.name)
            result = subprocess.run(["op", "read", field_value], capture_output=True)
            if result.returncode != 0:
                err = result.stderr.decode("utf-8")
                msg = f"Could not read secret from 1Password: {err}"
                raise ValueError(msg)
            secret = result.stdout.decode("utf-8").strip()
            return secret

        def secret_setter(self: models.Model, value: str) -> None:
            raise NotImplementedError("OPField does not support setting secret values")

        secret = property(secret_getter, secret_setter)
        return op_uri, secret

    @override
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.vaults is not None:
            kwargs["vaults"] = self.vaults
        return name, path, args, kwargs
