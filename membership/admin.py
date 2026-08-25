from django.contrib import admin

from .models import Membership


class MembershipAdmin(admin.ModelAdmin):
    fields = ("role", "member", "organization")
    list_display = ("member", "organization", "role")
    list_filter = ("role", "organization")
    list_per_page = 50
    sortable_by = (
        "created_at",
        "organization",
    )


admin.site.register(Membership, MembershipAdmin)
