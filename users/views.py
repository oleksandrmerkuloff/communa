from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import (
    UserReaderSerializer,
    UserWriterSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return UserReaderSerializer
        return UserWriterSerializer

    @action(detail=False, methods=["get", "patch", "delete"], permission_classes=[IsAuthenticated])
    def me(self, request):
        # Maybe later change from action to independant view for "me" path
        if request.method == "GET":
            serializer = UserReaderSerializer(request.user)
            return Response(serializer.data)
        elif request.method == "PATCH":
            serializer = UpdateUserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        user = request.user
        user.delete()
        return Response(
            {"message": "Your account has been deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods="post", permission_classes=[IsAuthenticated], url_path="change-password")
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
