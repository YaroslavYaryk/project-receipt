from django.urls import path
from .views import (
    index,
    create_receipt,
    create_project,
    edit_project,
    delete_project,
    get_projects_list,
    edit_receipt,
    delete_receipt,
    send_receipt_to_email,
    download_receipt,
)

urlpatterns = [
    path("", index, name="home"),
    path("send_email/", send_receipt_to_email, name="send_receipt_to_email"),
    path(
        "send_email/<email>/<receipt_id>/",
        send_receipt_to_email,
        name="send_receipt_to_email2",
    ),
    path("create_receipt/", create_receipt, name="create_receipt"),
    path("edit_receipt/<receipt_id>/", edit_receipt, name="edit_receipt"),
    path("delete_receipt/<receipt_id>/", delete_receipt, name="delete_receipt"),
    path("create_project/", create_project, name="create_project"),
    path("edit_project/<project_id>/", edit_project, name="edit_project"),
    path("delete_project/<project_id>/", delete_project, name="delete_project"),
    path("projects_list/", get_projects_list, name="get_projects_list"),
    path("download_receipt/", download_receipt, name="download_receipt"),
    path("download_receipt/<receipt_id>/", download_receipt, name="download_receipt2"),
]
