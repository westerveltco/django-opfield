from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from django_opfield.conf import OPFIELD_SETTINGS_NAME
from django_opfield.conf import _get_user_setting
from django_opfield.conf import app_settings


class TestGetUserSettings:
    def test_not_set(self):
        assert _get_user_setting("TEST_SETTING") is None

    @override_settings(**{OPFIELD_SETTINGS_NAME: {"TEST_SETTING": "test value"}})
    def test_set_in_settings(self):
        assert _get_user_setting("TEST_SETTING") == "test value"

    @patch.dict(os.environ, {"TEST_SETTING": "test value"})
    def test_set_in_env(self):
        assert _get_user_setting("TEST_SETTING") == "test value"


class TestGetOpCLIPath:
    @pytest.fixture(autouse=True)
    def setup(self):
        env = {k: v for k, v in os.environ.items() if k not in {"OP_CLI_PATH"}}
        with patch.dict(os.environ, env, clear=True):
            yield

    @patch("shutil.which")
    def test_default(self, mock_which):
        mock_which.return_value = None

        with pytest.raises(ImportError) as exc_info:
            assert app_settings.get_op_cli_path()

        assert "Could not find the 'op' CLI command" in str(exc_info.value)

    @override_settings(**{OPFIELD_SETTINGS_NAME: {"OP_CLI_PATH": "path/to/op"}})
    def test_user_setting(self):
        assert "path/to/op" in str(app_settings.get_op_cli_path())

    @patch.dict(os.environ, {"OP_CLI_PATH": "path/to/op"})
    def test_env_var(self):
        assert "path/to/op" in str(app_settings.get_op_cli_path())

    @patch("shutil.which")
    def test_shutil_which(self, mock_which):
        mock_which.return_value = "path/to/op"

        assert "path/to/op" in str(app_settings.get_op_cli_path())


class TestOpCommandTimeout:
    def test_default(self):
        assert app_settings.OP_COMMAND_TIMEOUT == 5

    @override_settings(**{OPFIELD_SETTINGS_NAME: {"OP_COMMAND_TIMEOUT": 10}})
    def test_user_setting(self):
        assert app_settings.OP_COMMAND_TIMEOUT == 10


class TestGetOpServiceAccountToken:
    def test_default(self):
        with pytest.raises(ImproperlyConfigured) as exc_info:
            assert app_settings.get_op_service_account_token()

        assert "OP_SERVICE_ACCOUNT_TOKEN is not set" in str(exc_info.value)

    @override_settings(**{OPFIELD_SETTINGS_NAME: {"OP_SERVICE_ACCOUNT_TOKEN": "token"}})
    def test_user_setting(self):
        assert app_settings.get_op_service_account_token() == "token"

    @patch.dict(os.environ, {"OP_SERVICE_ACCOUNT_TOKEN": "token"})
    def test_env_var(self):
        assert app_settings.get_op_service_account_token() == "token"
