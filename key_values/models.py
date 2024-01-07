from django.db import models


class KeyValues(models.Model):
    data = models.JSONField()
    key = models.TextField(unique=True)
