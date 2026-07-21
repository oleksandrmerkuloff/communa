from rest_framework.viewsets import ModelViewSet

from .models import Post, Tag, NewsAttachment
from .serializers import PostReaderSerializer, PostWriterSerializer, TagSerializer, TagShortSerializer, NewsAttachmentSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()

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
