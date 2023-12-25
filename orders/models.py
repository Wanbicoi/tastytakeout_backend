from django.db import models
from foods.models import Food
from users.models import User
from stores.models import Store
from django.utils import timezone


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


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    ORDER_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(max_length=8, choices=ORDER_STATUS_CHOICES)
    total = models.IntegerField()
    created_at = models.DateTimeField()
    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("BANKING", "Banking"),
    ]
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES)


class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
