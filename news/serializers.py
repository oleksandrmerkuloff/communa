from rest_framework import serializers

from .models import Tag, Post, NewsAttachment
from organization.serializers import OrganizationReaderSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["id"]

class TagShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name",)

class NewsAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        fields = "__all__"
        read_only_fields = ["id"]

class PostWriterSerializer(serializers.ModelSerializer):
    attachments = NewsAttachmentSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ("title", "content", "status", "tags", "organization", "attachments")
    
    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        attachments_data = validated_data.pop("attachments", [])

        post = Post.objects.create(**validated_data)
        post.tags.set(tags)

        for attachment_data in attachments_data:
            NewsAttachment.objects.create(post=post, **attachment_data)
        
        return post

class PostReaderSerializer(serializers.ModelSerializer):
    attachments = NewsAttachmentSerializer(many=True, read_only=True)
    tags = TagShortSerializer(many=True, read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
