from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


# class UserManager(BaseUserManager):
# def create_user(self, email: str, password: str | None = None, **other_fields):
#     user = User(email=email, **other_fields)
#
#     if password:
#         user.set_password(password)
#     else:
#         user.set_unusable_password()
#
#     user.save()
#     return user


class User(AbstractUser):
    # remove default fields
    first_name = None
    last_name = None

    # username = models.TextField()
    # password = models.TextField()
    # auth_id = models.IntegerField()  # External Provider Id

    ROLE_CHOICES = [
        ("BUYER", "Buyer"),
        ("SELLER", "Seller"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    PIN = models.TextField(null=True)
    phone = models.TextField()

    avatar_url = models.TextField()
    name = models.TextField()
    bio = models.TextField(null=True)
    address = models.TextField(null=True)
    date_of_birth = models.DateTimeField(default=timezone.now)
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="MALE")

    liked_foods = models.ManyToManyField("foods.Food")
    liked_stores = models.ManyToManyField("stores.Store")

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name