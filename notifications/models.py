from django.db import models
from rest_framework.fields import timezone

from users.models import User


class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField()
    body = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
