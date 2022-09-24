from django.urls import path
from .views import index, send, create_receipt, create_project, get_projects_list

urlpatterns = [
    path("", index, name="home"),
    path("send/", send, name="send"),
    path("create_receipt/", create_receipt, name="create_receipt"),
    path("create_project/", create_project, name="create_project"),
    path("projects_list/", get_projects_list, name="get_projects_list"),
]
