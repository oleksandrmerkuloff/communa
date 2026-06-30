from django.db import transaction
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

        with transaction.atomic():

            post = Post.objects.create(**validated_data)
            post.tags.set(tags)
    
            for attachment_data in attachments_data:
                NewsAttachment.objects.create(post=post, **attachment_data)
        
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", [])
        attachments_data = validated_data.pop("attachments", [])
        
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if tags :
                instance.tags.set(tags)
            
            existing_attachments = {att.id: att for att in instance.attachments.all()}
            keep_attachment_ids = []
            
            if attachments_data:

                for attachment_item in attachments_data:
                    attachment_id = attachment_item.get('id', None)

                    if attachment_id in existing_attachments:
                        att_instance = existing_attachments[attachment_id]
                        for key, value in attachment_item.items():
                            setattr(att_instance, key, value)
                        att_instance.save()
                        keep_attachment_ids.append(att_instance.id)
                    else:
                        new_att = NewsAttachment.objects.create(post=instance, **attachment_item)
                        keep_attachment_ids.append(new_att.id)

            for att_id, att_instance in existing_attachments.items():
                if att_id not in keep_attachment_ids:
                    att_instance.delete()

        return instance


class PostReaderSerializer(serializers.ModelSerializer):
    attachments = NewsAttachmentSerializer(many=True, read_only=True)
    tags = TagShortSerializer(many=True, read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
