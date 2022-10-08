from rest_framework import status
from photoproject.models import Category, ProjectReceipts, Receipt
from .serializers import (
    CategoryPostSerializer,
    CategorySerializer,
    ProjectReportSerializer,
    ProjectSerializer,
    ProjectPostSerializer,
    ReceiptPostSerializer,
    ReceiptSerializer,
    ReceiptFileSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from photoproject.tasks import save_pdf, send_email_with_receipt

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    # RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.decorators import action

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from photoproject.services import handle_receipt


class ProjectListAPIView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head"]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = handle_receipt.get_projects_for_user(request.user)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = handle_receipt.get_projects_for_user(request.user).get(pk=pk)
        serializer = ProjectSerializer(queryset)
        return Response(serializer.data)


class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {**request.data, "user": request.user.id}
        print(data)
        serializer = ProjectPostSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            return Response({**serializer.data, "id": instance.id})

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        instance = handle_receipt.get_project_by_id(pk)
        data = {**request.data, "user": request.user.id}
        serializer = ProjectPostSerializer(data=data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()

            return Response({**serializer.data, "id": instance.id})

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = handle_receipt.get_project_by_id(pk)
        try:
            data = {"id": instance.id, "message": "successful"}
            instance.delete()
            return Response(data)
        except Exception as ex:
            return Response({"message": str(ex)})


class CategoryListAPIView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = Category.objects.get(pk=pk)
        serializer = CategorySerializer(queryset)
        return Response(serializer.data)


class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {**request.data}
        serializer = CategoryPostSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            return Response({**serializer.data, "id": instance.id})

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        instance = handle_receipt.get_category_by_id(pk)
        data = {**request.data}
        serializer = CategoryPostSerializer(data=data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()

            return Response({**serializer.data, "id": instance.id})

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = handle_receipt.get_category_by_id(pk)
        try:
            data = {"id": instance.id, "message": "successful"}
            instance.delete()
            return Response(data)
        except Exception as ex:
            return Response({"message": str(ex)})


class ReceiptListAPIView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = handle_receipt.get_receipts_by_user(request.user)
        serializer = ReceiptSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = handle_receipt.get_receipts_by_user(request.user).get(pk=pk)
        serializer = ReceiptSerializer(queryset)
        return Response(serializer.data)


class ReceiptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = {
            "company": request.data["company"],
            "date": request.data["date"],
            "price": request.data["price"],
            "description": request.data["description"],
            "business": request.data["business"],
            "persons": request.data["persons"],
            "comment": request.data.get("comment"),
            "user": request.user.id,
        }
        serializer = ReceiptPostSerializer(data=data)

        # new_serializer = ReceiptSerializer(Receipt.objects.get(pk=10))
        if serializer.is_valid():
            instance = serializer.save()
            handle_receipt.add_project(
                instance, request.data["project"], request.data["project_id"]
            )
            handle_receipt.add_category(
                instance, request.data["category"], request.data["category_id"]
            )

            if request.data.get("photos"):
                handle_receipt.save_images(instance, request.data)
            instance.save()
            try:
                save_pdf.delay(instance.id)
            except Exception as ex:
                print(ex)
            new_serializer = ReceiptSerializer(
                instance=Receipt.objects.get(pk=instance.id)
            )
            return Response(new_serializer.data)
        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        instance = handle_receipt.get_receipt_by_id(pk)
        data = {
            "company": request.data["company"],
            "date": request.data["date"],
            "price": request.data["price"],
            "description": request.data["description"],
            "business": request.data["business"],
            "persons": request.data["persons"],
            "comment": request.data.get("comment"),
            "user": request.user.id,
        }
        serializer = ReceiptPostSerializer(data=data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()
            handle_receipt.add_project(
                instance, request.data["project"], request.data["project_id"]
            )
            handle_receipt.add_category(
                instance, request.data["category"], request.data["category_id"]
            )

            if request.data.get("photos"):
                handle_receipt.save_images(instance, request.data)
            instance.save()
            try:
                save_pdf.delay(instance.id)
            except Exception as ex:
                print(ex)
            new_serializer = ReceiptSerializer(
                instance=Receipt.objects.get(pk=instance.id)
            )
            return Response(new_serializer.data)

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = handle_receipt.get_receipt_by_id(pk)
        try:
            data = {"id": instance.id, "message": "successful"}
            instance.delete()
            return Response(data)
        except Exception as ex:
            return Response({"error": str(ex)})


class ProjectReportsListAPIView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head"]

    def list(self, request, proj):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = ProjectReceipts.objects.filter(project__id=proj)
        serializer = ProjectReportSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = ProjectReceipts.objects.get(id=pk)
        serializer = ProjectReportSerializer(queryset)
        return Response(serializer.data)


@api_view(["GET"])
def get_receipt_file(request, receipt):

    try:
        instance = Receipt.objects.get(pk=receipt)
        serializer = ReceiptFileSerializer(instance=instance)

        return Response(serializer.data)
    except Exception as ex:
        return Response({"message": str(ex)})
