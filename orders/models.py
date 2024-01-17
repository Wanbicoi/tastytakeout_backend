from django.db import models
from foods.models import Food
from users.models import User
from stores.models import Store
from django.utils import timezone


class Event(models.Model):
    imageUrl = models.CharField()
    name = models.CharField()
    description = models.CharField()
    begin = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)


class Voucher(models.Model):
    code = models.TextField(unique=True)
    name = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    used_quantity = models.IntegerField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    DISCOUNT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("PERCENT", "Percent"),
    ]
    discount_amount = models.IntegerField()
    discount_type = models.CharField(max_length=8, choices=DISCOUNT_TYPE_CHOICES)
    max_price = models.IntegerField()
    min_price = models.IntegerField()

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="vouchers", null=True
    )


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    ORDER_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PREPARE", "Prepare"),
        ("DELIVERING", "Delivering"),
        ("COMPLETED", "Completed"),
    ]
    status = models.CharField(
        max_length=10, choices=ORDER_STATUS_CHOICES, default="PENDING"
    )
    total = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("BANKING", "Banking"),
    ]
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES)


class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="foods")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
