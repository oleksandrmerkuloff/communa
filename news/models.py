import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

#! later I need to import organization model from organization app

class Tag(models.Model):
    name = models.CharField(max_length=15)
    organization = models.ForeignKey("Organization", related_name="tags", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
        
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    

class Post(models.Model):
    class PostStatus(models.TextChoices):
        DRAFT = "D", _("Draft")
        PUBLISHED = "P", _("Published")
        ARCHIVED = "A", _("Archived")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=PostStatus, default=PostStatus.DRAFT)
    views = models.PositiveIntegerField(blank=True, default=0)
    tags = models.ManyToManyField(Tag, related_name="posts")
    organization = models.ForeignKey("Organization", related_name="posts", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]


class NewsAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="") # I'll add path later
    uploaded_at = models.DateTimeField(auto_now_add=True)

    #? maybe I'll add ordering here if I'll need to implement image circle for example
    # Here I'll connect the same lib as for a personal website

    class Meta:
        verbose_name = "News Attachment"
        verbose_name_plural = "News Attachments"
