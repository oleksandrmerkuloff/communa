from django.contrib import admin

from .models import Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_at")
    list_display_links = ("name",)
    list_filter = ("organization", "is_system",)
    list_per_page = 50
    search_fields = ("name",)
    sortable_by = ("organization", "create_at", "update_at")


admin.site.register(Role, RoleAdmin)