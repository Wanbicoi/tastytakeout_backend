from django.db import models


class User(models.Model):
    BUYER = "BUYER"
    SELLER = "SELLER"
    ROLE_CHOICES = [
        (BUYER, "Buyer"),
        (SELLER, "Seller"),
    ]

    username = models.TextField()
    password = models.TextField()
    auth_id = models.IntegerField()  # External Provider Id
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    PIN = models.TextField()

    avatar_url = models.TextField()
    name = models.TextField()
    bio = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    date_of_birth = models.DateTimeField()
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)


class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey("Food", on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Category(models.Model):
    name = models.TextField()


class Food(models.Model):
    store = models.ForeignKey("Store", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_urls = models.JSONField()  # Array of strings
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    rating = models.FloatField()


class FoodComment(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    image_url = models.TextField()
    address = models.TextField()
    email = models.TextField()
    license_image_url = models.TextField()
    owner_name = models.TextField()
    note = models.TextField()
    deny_reason = models.TextField()
    created_at = models.DateTimeField()
    STORE_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(max_length=8, choices=STORE_STATUS_CHOICES)


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher = models.ForeignKey("Voucher", on_delete=models.CASCADE, null=True)
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


class BuyerLikeFood(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class BuyerLikeStore(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class Voucher(models.Model):
    code = models.TextField(unique=True)
    name = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    used_quantity = models.IntegerField()
    end = models.DateTimeField()
    created_at = models.DateTimeField()
    DISCOUNT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("PERCENT", "Percent"),
    ]
    discount_amount = models.IntegerField()
    discount_type = models.CharField(max_length=8, choices=DISCOUNT_TYPE_CHOICES)
    max_price = models.IntegerField()
    min_price = models.IntegerField()


class FoodDiscount(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    DISCOUNT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("PERCENT", "Percent"),
    ]
    discount_amount = models.IntegerField()
    discount_type = models.CharField(max_length=8, choices=DISCOUNT_TYPE_CHOICES)
    end = models.DateTimeField()


class Chat(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    message = models.TextField()
    SENDER_CHOICES = [
        ("STORE", "Store"),
        ("BUYER", "Buyer"),
    ]
    sender = models.CharField(max_length=5, choices=SENDER_CHOICES)
    created_at = models.DateTimeField()
