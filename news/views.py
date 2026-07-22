from rest_framework.viewsets import ModelViewSet

from .models import Post, Tag, NewsAttachment
from .serializers import PostReaderSerializer, PostWriterSerializer, TagSerializer, TagShortSerializer, NewsAttachmentSerializer
from .permissions import CanEditTags, CanCreateTags, CanDeleteTags, CanDeleteNews, CanEditNews, CanViewNews, CanCreateNews


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [CanCreateTags]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditTags]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteTags]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return (
            Tag.objects
            .filter(organization__memberships__member=self.request.user)
            .select_related("organization")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TagShortSerializer
        return TagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_permissions(self):
            if self.action in ("list", "retrieve"):
                self.permission_classes = [CanViewNews]
            elif self.action == "create":
                self.permission_classes = [CanCreateNews]
            elif self.action in ("update", "partial_update"):
                self.permission_classes = [CanEditNews]
            elif self.action == "destroy":
                self.permission_classes = [CanDeleteNews]
            else:
                self.permission_classes = []
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return (
            Post.objects
            .filter(organization__memberships__member=self.request.user)
            .select_related("organization")
            .prefetch_related("tags", "attachments")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PostReaderSerializer
        return PostWriterSerializer
