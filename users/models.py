import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
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

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICE, default="Male", max_length=10, blank=True
    )
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICE, max_length=2, blank=True, default="ko"
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICE, max_length=3, blank=True, default="krw"
    )
    is_superhost = models.BooleanField(default=False, verbose_name="Is Superhost")
    bio = models.TextField(blank=True)
    email_confirmed = models.BooleanField(default=False)
    email_secret_key = models.CharField(max_length=120, default="", blank=True)

    def verify_email(self):
        if self.email_confirmed is False:
            secret = uuid.uuid4().hex
            self.email_secret_key = secret
            send_mail(
                "Verify Airbnb Account",
                f"Verify account, this is your secret: {secret}",
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
            )
        return
