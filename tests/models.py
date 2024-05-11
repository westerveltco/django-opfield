from __future__ import annotations

from django.db import models

from django_opfield.fields import OPField


class TestModel(models.Model):
    op_uri = OPField()
