from django.db import models
from users.models import User
from django.utils import timezone


class Store(models.Model):
    owner = models.ForeignKey(User, related_name="stores", on_delete=models.CASCADE)
    name = models.TextField()
    image_url = models.TextField(null=True)
    phone = models.TextField(null=True)
    address = models.TextField(null=True)
    email = models.TextField(null=True)
    license_image_url = models.TextField(null=True)
    owner_name = models.TextField(null=True)
    note = models.TextField(null=True)
    deny_reason = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    STORE_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(
        max_length=8, choices=STORE_STATUS_CHOICES, default="PENDING"
    )
