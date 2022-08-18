from django.contrib import admin
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    """Custom User Admin"""

    list_display = (
        "username",
        "email",
        "gender",
        "language",
        "currency",
        "is_superhost",
    )
    list_filter = ("language", "currency", "is_superhost")
