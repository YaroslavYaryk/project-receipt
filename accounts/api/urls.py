from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView
from django.urls import re_path, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    CreateUserAPIView,
    LogoutUserAPIView,
    UserApiView,
    CustomAuthToken,
)

urlpatterns = [
    path("create/", CustomUserCreate.as_view(), name="create_user"),
    path("logout/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
    re_path(r"^auth/login/$", CustomAuthToken.as_view(), name="auth_user_login"),
    re_path(r"^auth/register/$", CreateUserAPIView.as_view(), name="auth_user_create"),
    re_path(r"^auth/logout/$", LogoutUserAPIView.as_view(), name="auth_user_logout"),
    path("user_profile/", UserApiView.as_view(), name="user_profile"),
    path("user_base_edit/", UserApiView.as_view(), name="user_base_edit"),
    #     path("edit_living_place/", change_place_info, name="change_place_info"),
    #     path("edit_warehouse/", change_warehouse_info, name="change_warehouse_info"),
    #     path(
    #         "edit_delivery_type/",
    #         change_delivery_type_info,
    #         name="change_delivery_type_info",
    #     ),
]
