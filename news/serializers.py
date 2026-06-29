from rest_framework import serializers

from models import Tag, Post, NewsAttachment


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
    organization = "OrganizationShortSerializer(read_only=True)" # It's dummy code until I'll create users and auth modules
    class Meta:
        model = Post
        fields = "__all__"


# class DummyOrganizationSerializer(serializers.Serializer):
    # """Dummy serializer for example"""
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=50)
# 
# 
# class TagSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=15)
    # organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
# 
    # def create(self, validated_data):
        # return Tag.objects.create(**validated_data)
    # 
    # def update(self, instance, validated_data):
        # instance.name = validated_data.get("name", instance.name).title()
        # instance.save()
        # return instance
# 
# 
# class PostReaderSerializer(serializers.Serializer):
    # id = serializers.UUIDField()
    # title = serializers.CharField()
    # content = serializers.CharField()
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()
    # status = serializers.ChoiceField(choices=[
        # ("D", "Draf",),
        # ("P", "Published",),
        # ("A", "Archived")
        # ])
    # views = serializers.IntegerField()
    # tags = serializers.StringRelatedField(many=True)
    # organization = DummyOrganizationSerializer()
# 
# 
# class PostWriteSerializer(serializers.Serializer):
    # title = serializers.CharField(max_length=50)
    # content = serializers.CharField(allow_blank=True, allow_null=True)
    # status = serializers.ChoiceField(choices=[
        # ("D", "Draf",),
        # ("P", "Published",),
        # ("A", "Archived")
        # ])
    # tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    # organization = serializers.PrimaryKeyRelatedField(many=True, queryset=Organization.objects.all())
# 
    # def create(self, validated_data):
        # title = validated_data.pop("title", None).title()
        # tags = validated_data.pop("tags", [])
# 
        # post = Post.objects.create(title=title, **validated_data)
        # post.tags.set(tags)
        # return post
# 
    # def update(self, instance, validated_data):
        # tags = validated_data.pop("tags", None)
# 
        # instance.title = validated_data.get("title", instance.title).title()
        # instance.content = validated_data.get("content", instance.content)
        # instance.status = validated_data.get("status", instance.status)
        # instance.save()
# 
        # if tags is not None:
            # instance.tags.set(tags)
# 
        # return instance
# 
# 
# class NewsAttachmentSerializer(serializers.Serializer):
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    # id = serializers.IntegerField(read_only=True)
    # file = serializers.FileField()
    # uploaded_at = serializers.DateTimeField(read_only=True)
# 
    # def create(self, validated_data):
        # return NewsAttachment.objects.create(**validated_data)
    # 
    # def update(self, instance, validated_data):
        # instance.post = validated_data.get("post", instance.post)
        # instance.file = validated_data.get("file", instance.file)
        # instance.save()
        # return instance
# 