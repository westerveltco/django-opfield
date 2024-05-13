from __future__ import annotations

import os
from unittest.mock import ANY
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.db import models

from django_opfield.fields import OPField
from django_opfield.validators import OPURIValidator

from .models import TestModel


def test_init_with_defaults():
    field = OPField()

    assert field.max_length == 255
    assert field.vaults is None
    assert isinstance(field, models.CharField)


def test_init_with_max_length():
    field = OPField(max_length=10)

    assert field.max_length == 10


@pytest.mark.parametrize(
    "vaults",
    [
        None,
        ["vault33"],
        ["vault33", "vault31"],
    ],
)
def test_init_with_vaults(vaults):
    field = OPField(vaults=vaults)

    assert field.vaults == vaults


def test_init_validator():
    field = OPField()

    validators = [type(validator) for validator in field.validators]

    assert OPURIValidator in validators


def test_deconstruct_default():
    field = OPField()

    name, path, args, kwargs = field.deconstruct()

    assert name is None
    assert path == "django_opfield.fields.OPField"
    assert args == []
    assert kwargs.get("vaults") is None
    assert kwargs.get("max_length") == 255


def test_deconstruct_with_max_length():
    field = OPField(max_length=10)

    name, path, args, kwargs = field.deconstruct()

    assert kwargs.get("max_length") == 10


def test_deconstruct_with_vaults():
    field = OPField(vaults=["vault33", "vault31"])
    name, path, args, kwargs = field.deconstruct()

    assert kwargs.get("vaults") == ["vault33", "vault31"]


@patch("subprocess.run")
@patch.dict(os.environ, {"OP_SERVICE_ACCOUNT_TOKEN": "token"})
def test_get_secret(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = b"secret value"

    model = TestModel(op_uri="op://vault/item/field")

    print("env OP_CLI_PATH", os.environ.get("OP_CLI_PATH"))

    secret = model.op_uri_secret

    mock_run.assert_called_once_with(
        [ANY, "read", "op://vault/item/field"], capture_output=True
    )
    assert secret == "secret value"


@patch("subprocess.run")
def test_get_secret_no_token(mock_run):
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = b"error message"

    model = TestModel(op_uri="op://vault/item/field")

    with pytest.raises(ValueError) as exc_info:
        _ = model.op_uri_secret

    assert "OP_SERVICE_ACCOUNT_TOKEN is not set" in str(exc_info.value)


@patch("subprocess.run")
@patch.dict(os.environ, {"OP_SERVICE_ACCOUNT_TOKEN": "token"})
def test_get_secret_error(mock_run):
    mock_run.return_value.returncode = 1
    mock_run.return_value.stderr = b"error message"

    model = TestModel(op_uri="op://vault/item/field")

    print("env OP_CLI_PATH", os.environ.get("OP_CLI_PATH"))

    with pytest.raises(ValueError) as exc_info:
        _ = model.op_uri_secret

    assert "Could not read secret from 1Password" in str(exc_info.value)


@patch("shutil.which")
@patch.dict(os.environ, {"OP_SERVICE_ACCOUNT_TOKEN": "token"})
def test_get_secret_command_not_available(mock_which, db):
    mock_which.return_value = None

    model = TestModel(op_uri="op://vault/item/field")

    print("env OP_CLI_PATH", os.environ.get("OP_CLI_PATH"))

    with pytest.raises(ImportError) as excinfo:
        _ = model.op_uri_secret

    assert "Could not find the 'op' CLI command" in str(excinfo.value)


@patch("subprocess.run")
@patch.dict(os.environ, {"OP_SERVICE_ACCOUNT_TOKEN": "token"})
def test_set_secret_failure(mock_run):
    model = TestModel(op_uri="op://vault/item/field")

    with pytest.raises(NotImplementedError) as exc_info:
        model.op_uri_secret = "new secret"
        model.save()

    assert "OPField does not support setting secret value" in str(exc_info.value)


@pytest.mark.parametrize(
    "valid_uri",
    [
        "op://vault/item/field",
        "op://vault/item/section/field",
    ],
)
def test_model_with_valid_op_uri(valid_uri, db):
    model = TestModel(op_uri=valid_uri)
    model.full_clean()
    model.save()

    assert model.op_uri == valid_uri


@pytest.mark.parametrize(
    "invalid_uri",
    [
        "invalid_uri",
        "op://",
        "op://vault",
        "op://vault/item",
        "https://example.com",
    ],
)
def test_model_with_invalid_op_uri(invalid_uri, db):
    model = TestModel(op_uri=invalid_uri)

    with pytest.raises(ValidationError) as excinfo:
        model.full_clean()
        model.save()

    assert "op_uri" in str(excinfo.value)
