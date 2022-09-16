from django.contrib.auth import authenticate, login, logout, views
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from . import forms


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


class LogoutView(views.LogoutView):

    next_page = reverse_lazy("core:home")


# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     password = form.cleaned_data.get("password")
    #     user = authenticate(username=email, password=password)
    #     if user is not None:
    #         login(self.request, user)
    #     return super().form_valid(form)
