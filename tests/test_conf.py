from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from django.test import override_settings

from django_opfield.conf import OPFIELD_SETTINGS_NAME
from django_opfield.conf import app_settings


class TestGetUserSettings:
    def test_not_set(self):
        assert app_settings._get_user_settings("TEST_SETTING") is None

    @override_settings(**{OPFIELD_SETTINGS_NAME: {"TEST_SETTING": "test value"}})
    def test_set_in_settings(self):
        assert app_settings._get_user_settings("TEST_SETTING") == "test value"

    @patch.dict(os.environ, {"TEST_SETTING": "test value"})
    def test_set_in_env(self):
        assert app_settings._get_user_settings("TEST_SETTING") == "test value"


@patch.dict(os.environ, {"OP_CLI_PATH": ""})
class TestOPCliPath:
    @patch("shutil.which")
    def test_default(self, mock_which):
        mock_which.return_value = None

        with pytest.raises(ImportError):
            assert app_settings.OP_CLI_PATH

    @override_settings(**{OPFIELD_SETTINGS_NAME: {"OP_CLI_PATH": "path/to/op"}})
    def test_user_setting(self):
        assert "path/to/op" in str(app_settings.OP_CLI_PATH)

    @patch.dict(os.environ, {"OP_CLI_PATH": "path/to/op"})
    def test_env_var(self):
        assert "path/to/op" in str(app_settings.OP_CLI_PATH)

    @patch("shutil.which")
    def test_shutil_which(self, mock_which):
        mock_which.return_value = "path/to/op"

        assert "path/to/op" in str(app_settings.OP_CLI_PATH)
