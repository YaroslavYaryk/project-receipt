from django.urls import path
from .views import LoginUser, RegisterUser, LogoutUser
from .views import get_profile_edit, get_profile, change_password
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("profile/<user_id>/", get_profile, name="profile"),
    path("profile_edit/<user_id>/", get_profile_edit, name="edit_profile"),
    path("change_password/", change_password, name="change_password"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="reset_password",
    ),
    path(
        "password_reset_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
