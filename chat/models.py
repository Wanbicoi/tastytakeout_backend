from django.db import models
from users.models import User
from django.utils import timezone
from stores.models import Store


class Chat(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    message = models.TextField()
    SENDER_CHOICES = [
        ("STORE", "Store"),
        ("BUYER", "Buyer"),
    ]
    sender = models.CharField(max_length=5, choices=SENDER_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
