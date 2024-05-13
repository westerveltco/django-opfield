from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from django.test import override_settings

from django_opfield.conf import app_settings


class TestOPCliPath:
    def test_default(self):
        assert app_settings.OP_CLI_PATH is None

    @override_settings(DJANGO_OPFIELD={"OP_CLI_PATH": "path/to/op"})
    def test_custom(self):
        assert app_settings.OP_CLI_PATH == "path/to/op"
        assert app_settings.get_op_cli_path() == Path("path/to/op")

    @patch.dict(os.environ, {"OP_CLI_PATH": "path/to/op"})
    def test_env_var(self):
        assert app_settings.OP_CLI_PATH is None
        assert app_settings.get_op_cli_path() == Path("path/to/op")

    @patch("shutil.which")
    def test_shutil_which(self, mock_which):
        mock_which.return_value = "path/to/op"

        assert app_settings.OP_CLI_PATH is None
        assert app_settings.get_op_cli_path() == Path("path/to/op")

    @patch("shutil.which")
    def test_get_op_cli_path_none(self, mock_which):
        mock_which.return_value = None

        with pytest.raises(ImportError):
            assert app_settings.get_op_cli_path()
