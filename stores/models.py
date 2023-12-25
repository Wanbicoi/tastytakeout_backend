from django.db import models
from users.models import User
from django.utils import timezone


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    image_url = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    email = models.TextField()
    license_image_url = models.TextField()
    owner_name = models.TextField()
    note = models.TextField()
    deny_reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    STORE_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(
        max_length=8, choices=STORE_STATUS_CHOICES, default="PENDING"
    )
