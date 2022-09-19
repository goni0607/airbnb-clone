from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "birthdate",
                    "language",
                    "currency",
                    "is_superhost",
                    "bio",
                    "email_confirmed",
                    "email_secret_key",
                    "login_method",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "gender",
        "language",
        "currency",
        "is_superhost",
        "email_confirmed",
        "email_secret_key",
        "login_method",
    )
    list_filter = ("language", "currency", "is_superhost")
