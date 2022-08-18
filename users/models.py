from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """Custom User Model"""

    GENDER_CHOICE = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    LANGUAGE_CHOICE = [
        ("en", "English"),
        ("ko", "Korean"),
    ]
    CURRENCY_CHOICE = [
        ("usd", "USD"),
        ("krw", "KRW"),
    ]

    avatar = models.ImageField(null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICE, default="Male", max_length=10, null=True, blank=True
    )
    birthdate = models.DateField(null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICE, max_length=2, null=True, blank=True
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICE, max_length=3, null=True, blank=True
    )
    is_superhost = models.BooleanField(default=False, verbose_name="Is Superhost")
    bio = models.TextField(default="", blank=True)
