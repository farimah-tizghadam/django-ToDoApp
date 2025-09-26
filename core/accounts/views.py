from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    # fields = "username","password"
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy("task_list")



class RegisterPageView(CreateView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = '/accounts/login/'
