from django.contrib import admin

from .models import Tag, Post, NewsAttachment


class NewsAttachmentInline(admin.TabularInline):
    model = NewsAttachment
    extra = 1



class PostAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = [
        "title",
        "created_at",
        "status",
        "organization"
    ]
    list_display_links = ["title",]
    list_filter = ["tags",]
    list_per_page = 50
    readonly_fields = ["created_at", "updated_at",]
    search_fields = ["title", "organization__name",]
    sortable_by = ["created_at", "updated_at", "organization__name",]
    inlines = [
        NewsAttachmentInline,
    ]


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(NewsAttachment)
