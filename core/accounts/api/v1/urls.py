from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api-V1"

urlpatterns = [
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    path("token/login/", views.CustomAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    # jwt path
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    # change password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # reset password
    path(
        "password-reset/", views.ResetPasswordApiView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/<str:token>",
        views.ConfirmResetPasswordApiView.as_view(),
        name="password_reset_confirm",
    ),
    # confirm user by email (user activation)
    path(
        "activation/confirm/<str:token>/",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # profile
    path("profile/", views.ProfileApiView.as_view(), name="profile"),
]
