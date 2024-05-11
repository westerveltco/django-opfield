from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError

from django_opfield.validators import OPURIValidator


@pytest.mark.parametrize(
    "valid_uri",
    [
        "op://vault/item/field",
        "op://vault/item/section/field",
    ],
)
def test_valid_uri(valid_uri):
    validator = OPURIValidator()

    assert validator(valid_uri) is None


@pytest.mark.parametrize(
    "invalid_uri",
    [
        "op://",
        "op://vault",
        "op://vault/item",
        "https://example.com",
    ],
)
def test_invalid_uri(invalid_uri):
    validator = OPURIValidator()

    with pytest.raises(ValidationError):
        assert validator(invalid_uri)


@pytest.mark.parametrize(
    "valid_uri",
    [
        "op://vault/item/field",
        "op://vault/item/section/field",
    ],
)
def test_valid_uri_with_vault(valid_uri):
    validator = OPURIValidator(vaults=["vault"])

    assert validator(valid_uri) is None


@pytest.mark.parametrize(
    "valid_uri",
    [
        "op://vault/item/field",
        "op://vault/item/section/field",
    ],
)
def test_valid_uri_with_mismatched_vault(valid_uri):
    validator = OPURIValidator(vaults=["invalid"])

    with pytest.raises(ValidationError):
        assert validator(valid_uri)


@pytest.mark.parametrize(
    "invalid_input",
    [
        1,
        "a" * 2048,
    ],
)
def test_invalid_input(invalid_input):
    validator = OPURIValidator()

    with pytest.raises(ValidationError):
        assert validator(invalid_input)
