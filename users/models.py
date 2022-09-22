import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags


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

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    email = models.EmailField(unique=True)
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
    login_method = models.CharField(
        max_length=10, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_confirmed is False:
            secret = uuid.uuid4().hex
            self.email_secret_key = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            # send_mail이 오류가 발생하여 print()로 대체함.
            print(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_HOST_USER,
                [self.email],
                html_message,
            )
            # send_mail(
            #     "Verify Airbnb Account",
            #     strip_tags(html_message),
            #     settings.EMAIL_HOST_USER,
            #     [self.email],
            #     fail_silently=False,
            #     html_message=html_message,
            # )
            self.save()
        return

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
