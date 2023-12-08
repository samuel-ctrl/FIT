from django.urls import path
from .views import (
    LoginView,
    VerifyOTPView,
    UserDetailsView,
    TokenRefreshView,
)


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("verify_otp", VerifyOTPView.as_view(), name="verify otp"),
    path("details", UserDetailsView.as_view(), name="User Details"),
    path("token/refresh", TokenRefreshView.as_view(), name="token refresh"),
]
