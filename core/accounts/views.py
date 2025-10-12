from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm


class CustomLoginView(LoginView):
    """
    a view for login page
    """

    template_name = "accounts/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task:task_list")


class RegisterPageView(CreateView):
    """
    a view for sing up page
    """

    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = "/accounts/login/"
