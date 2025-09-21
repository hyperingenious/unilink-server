from django.urls import path
from .views import RegisterView, LoginView, DeleteAccountView, VerifyEmailView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("delete/", DeleteAccountView.as_view(), name="delete"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]