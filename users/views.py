from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import (
    UserReaderSerializer,
    UserWriterSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return UserReaderSerializer
        return UserWriterSerializer