from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    CustomUserSerializer,
    UserEditBaseSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from .serializers import CreateUserSerializer, UserSerializer
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import (
    check_password,
)
from django.contrib.auth import get_user_model


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format="json"):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # We create a token than will be used for future auth
            # serializer.instance.username = request.data.get("username")
            # serializer.instance.save()
            token = Token.objects.create(user=serializer.instance)
            user = {"user_id": serializer.instance.id}
            token_data = {"token": token.key}
            return Response(
                {**serializer.data, **token_data, **user},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except IntegrityError as err:
            return Response({"message": str(err)}, status.HTTP_401_UNAUTHORIZED)


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserEditBaseSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            new_serializer = UserSerializer(instance)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)
        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        elem = get_user_model().objects.filter(
            email=request.data["email"],
        )
        if elem:
            user = elem.first()
            if check_password(request.data["password"], user.password):
                # user = serializer.validated_data["user"]
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "user_id": user.pk, "email": user.email}
                )
            else:
                return Response(
                    {"message": "Cannot log with this credentials"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
                raise Exception("Cannot log with this credentials")
        else:
            raise Exception("There is no such user")
