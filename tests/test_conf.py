from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from django.test import override_settings

from django_opfield.conf import app_settings


@patch.dict(os.environ, {"OP_CLI_PATH": ""})
class TestOPCliPath:
    @patch("shutil.which")
    def test_default(self, mock_which):
        mock_which.return_value = None

        with pytest.raises(ImportError):
            assert app_settings.OP_CLI_PATH

    @override_settings(DJANGO_OPFIELD={"OP_CLI_PATH": "path/to/op"})
    def test_user_setting(self):
        assert "path/to/op" in str(app_settings.OP_CLI_PATH)

    @patch.dict(os.environ, {"OP_CLI_PATH": "path/to/op"})
    def test_env_var(self):
        assert "path/to/op" in str(app_settings.OP_CLI_PATH)

    @patch("shutil.which")
    def test_shutil_which(self, mock_which):
        mock_which.return_value = "path/to/op"

        assert "path/to/op" in str(app_settings.OP_CLI_PATH)
