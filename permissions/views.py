from rest_framework import generics

from .models import Permission
from .serializers import PermissionReaderSerializer


class PermissionsListView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionReaderSerializer
    permission_classes = None
