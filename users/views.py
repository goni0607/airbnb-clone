import os
import requests
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse, reverse_lazy
from . import forms
from users import models as user_models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "triplek@weonit.co.kr"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret_key=key)
        user.email_confirmed = True
        user.email_secret_key = ""
        user.save()
    except user_models.User.DoesNotExist:
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scode=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is not None:
            payload = {
                "client_id": os.environ.get("GH_ID"),
                "client_secret": os.environ.get("GH_SECRET"),
                "code": code,
            }

            result = requests.post(
                "https://github.com/login/oauth/access_token",
                data=payload,
                headers={"Accept": "application/json"},
            )

            result_json = result.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get authorization token.")
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = user_models.User.objects.get(email=email)
                        if user.login_method != user_models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except user_models.User.DoesNotExist:
                        user = user_models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            bio=bio,
                            login_method=user_models.User.LOGIN_GITHUB,
                            email_confirmed=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile.")

        else:
            raise GithubException("Can't get authorization code.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_API")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=account_email"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_API")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        payload = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        token_request = requests.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
        )
        token_json = token_request.json()
        error = token_json.get("error")
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account", None)
        if kakao_account is None:
            raise KakaoException("Can't get Kakao Account Information.")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("Can't get email for Kakao account.")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = user_models.User.objects.get(email=email)
            if user.login_method != user_models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(
                email=email,
                first_name=nickname,
                login_method=user_models.User.LOGIN_KAKAO,
                username=email,
                email_confirmed=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = user_models.User
    context_object_name = "user_obj"


class UpdateProfileView(UpdateView):

    model = user_models.User
    template_name = "users/update-profile.html"
    fields = [
        "first_name",
        "last_name",
        "gender",
        "birthdate",
        "language",
        "currency",
        "bio",
    ]

    def get_object(self, queryset=None):
        return self.request.user

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


class PasswordChangeView(PasswordChangeView):

    template_name = "users/change-password.html"
