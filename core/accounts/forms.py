from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# get user model object
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    creating custom user form
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(forms.Form):
    """
    creating custom user login form
    """

    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(), label=_("Password"), required=True
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # Extract 'request' if provided
        super().__init__(*args, **kwargs)  # Call the parent class' init

    def get_user(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email).first()
        return user
