from django.urls import path
from .views import (
    ProjectListAPIView,
    ProjectAPIView,
    ReceiptListAPIView,
    ReceiptAPIView,
    ProjectReportsListAPIView,
)

urlpatterns = [
    # project
    path(
        "projects/",
        ProjectListAPIView.as_view({"get": "list"}),
        name="get_all_projects",
    ),
    path(
        "projects/<pk>/",
        ProjectListAPIView.as_view({"get": "retrieve"}),
        name="get_spec_project",
    ),
    path("project/create/", ProjectAPIView.as_view(), name="create_project"),
    path("project/<pk>/update/", ProjectAPIView.as_view(), name="update_project"),
    path("project/<pk>/delete/", ProjectAPIView.as_view(), name="delete_project"),
    # category
    # receipt
    path(
        "receipts/",
        ReceiptListAPIView.as_view({"get": "list"}),
        name="get_all_receipts",
    ),
    path(
        "receipts/<pk>/",
        ReceiptListAPIView.as_view({"get": "retrieve"}),
        name="get_spec_receipt",
    ),
    path("receipt/create/", ReceiptAPIView.as_view(), name="create_receipt"),
    path("receipt/update/<pk>/", ReceiptAPIView.as_view(), name="update_receipt"),
    path("receipt/delete/<pk>/", ReceiptAPIView.as_view(), name="delete_receipt"),
    # project reports
    path(
        "project_reports/<proj>/all/",
        ProjectReportsListAPIView.as_view({"get": "list"}),
        name="get_all_project_reports",
    ),
    path(
        "project_reports/<pk>/one/",
        ProjectReportsListAPIView.as_view({"get": "retrieve"}),
        name="get_spec_project_reports",
    ),
]
