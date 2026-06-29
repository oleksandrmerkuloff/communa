from django.contrib import admin

from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = [
        "name",
        "city",
        "post_index",
        "created_at"
    ]
    list_display_links = ["name",]
    list_filter = ["city",]
    list_per_page = 50
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["name", "city", "post_index"]
    sortable_by = ["created_at", "updated_at", "name"]


admin.site.register(Organization, OrganizationAdmin)
