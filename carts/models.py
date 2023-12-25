from django.db import models
from users.models import User
from foods.models import Food


class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
