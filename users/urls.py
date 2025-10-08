from django.urls import path
from .views import RegisterView, LoginView, DeleteAccountView, VerifyEmailView, FileUploadView, UserListView, UserProfileEditView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("delete/", DeleteAccountView.as_view(), name="delete"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("profile/edit/", UserProfileEditView.as_view(), name="profile-edit"),
]