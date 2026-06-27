from __future__ import annotations

from django.db import models

from django_opfield.fields import OPField


class OPFieldModel(models.Model):
    op_uri = OPField()

    def __str__(self) -> str:
        return self.op_uri
