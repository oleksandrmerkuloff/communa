from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .models import User
from .serializers import (
    UserReaderSerializer,
    UserWriterSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        if self.action in ("me", "change_password"):
            return [IsAuthenticated()]

        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "create":
            return UserWriterSerializer

        if self.action == "me":
            if self.request.method == "PATCH":
                return UpdateUserSerializer
            return UserReaderSerializer

        if self.action == "change_password":
            return ChangePasswordSerializer

        return UserReaderSerializer

    @action(detail=False, methods=["get", "patch", "delete"])
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post",], url_path="change-password")
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
