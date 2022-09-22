from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        print("LoggedOutOnlyView")
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "404 : Page not found.")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    print("LoggedInOnlyView")
    login_url = reverse_lazy("users:login")


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        print("EmailLoginOnlyView")
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "404 : Page not found.")
        return redirect(reverse("core:home"))
