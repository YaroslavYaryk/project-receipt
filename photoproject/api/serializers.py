from rest_framework.serializers import ModelSerializer
from django.utils.html import strip_tags
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
)
from photoproject.models import Project, Category, Receipt, ProjectReceipts
from decouple import config


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
        )


class ProjectPostSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ("name", "user")


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class CategoryPostSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "name"


class ReceiptSerializer(ModelSerializer):

    photos = SerializerMethodField()
    file_document = SerializerMethodField()

    class Meta:
        model = Receipt
        fields = "__all__"

    def get_photos(request, instance):
        return [
            {"id": elem.id, "url": f"{config('HOST')}:{config('PORT')}{elem.photo.url}"}
            for elem in instance.photos.all()
        ]

    def get_file_document(request, instance):
        return f"{config('HOST')}:{config('PORT')}{instance.file_document.url}"


class ReceiptPostSerializer(ModelSerializer):
    class Meta:
        model = Receipt
        exclude = "file_document", "photos"


class ProjectReportSerializer(ModelSerializer):

    file_document = SerializerMethodField()

    class Meta:
        model = ProjectReceipts
        fields = "__all__"

    def get_file_document(request, instance):
        return f"{config('HOST')}:{config('PORT')}{instance.file_document.url}"
