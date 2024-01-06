from django.db import models
from django.utils import timezone
from users.models import User


class Category(models.Model):
    name = models.TextField()


class Food(models.Model):
    store = models.ForeignKey(
        "stores.Store", related_name="foods", on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_urls = models.JSONField()  # Array of strings
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=5.0)


class FoodComment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name="comments", on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()


class FoodDiscount(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    DISCOUNT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("PERCENT", "Percent"),
    ]
    discount_amount = models.IntegerField()
    discount_type = models.CharField(max_length=8, choices=DISCOUNT_TYPE_CHOICES)
    end = models.DateTimeField()
