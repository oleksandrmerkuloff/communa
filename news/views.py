from rest_framework.viewsets import ModelViewSet

from .models import Post, Tag, NewsAttachment
from .serializers import PostReaderSerializer, PostWriterSerializer, TagSerializer, TagShortSerializer, NewsAttachmentSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()

    def get_queryset(self):
        return (
            Tag.objects
            .select_related("organization")
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TagShortSerializer
        return TagSerializer


class NewsAttachmentViewSet(ModelViewSet):
    queryset =  NewsAttachment.objects.all()
    serializer_class = NewsAttachmentSerializer

    def get_queryset(self):
        return (
            NewsAttachment.objects
            .select_related("post")
        )


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_queryset(self):
        return (
            Post.objects
            .select_related("organization")
            .prefetch_related("tags", "attachments")
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PostReaderSerializer
        return PostWriterSerializer
