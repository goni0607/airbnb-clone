from django.shortcuts import redirect
from django.urls import reverse


def go_home():
    return redirect(reverse("core:home"))
