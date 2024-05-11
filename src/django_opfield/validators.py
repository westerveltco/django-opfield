from __future__ import annotations

import re
import sys
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import (
    _lazy_re_compile,  # pyright: ignore[reportPrivateUsage]
)

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import (
        override,  # pyright: ignore[reportUnreachable]  # pragma: no cover
    )


@deconstructible
class OPURIValidator(RegexValidator):
    ul = "\u00a1-\uffff"  # Unicode letters range (must not be a raw string).

    op_path_re = (
        r"(?P<vault>[^/]+)"  # Vault: must be a non-empty string without slashes
        r"/(?P<item>[^/]+)"  # Item: must be a non-empty string without slashes
        r"(?:/(?P<section>[^/]+))?"  # Section: optional, non-empty string without slashes
        r"/(?P<field>[^/]+)"  # Field: must be a non-empty string without slashes
    )

    @property
    def op_regex(self) -> re.Pattern[str]:
        return _lazy_re_compile(
            r"^op://" + self.op_path_re + r"$",
            re.IGNORECASE,
        )

    message = "Enter a valid 1Password URI."
    schemes = ["op"]

    def __init__(self, vaults: list[str] | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.vaults = vaults if vaults is not None else []

    @override
    def __call__(self, value: Any) -> None:
        if not isinstance(value, str) or len(value) > 2048:
            raise ValidationError(self.message, code="invalid", params={"value": value})

        # Match the URL against the regex to validate structure
        match = self.op_regex.match(value)
        if not match:
            raise ValidationError(
                self.message, code="invalid_format", params={"value": value}
            )

        # Check if the vault is in the list of valid vaults
        vault = match.group("vault")
        if self.vaults and vault not in self.vaults:
            raise ValidationError(
                f"The vault '{vault}' is not a valid vault.", code="invalid_vault"
            )
