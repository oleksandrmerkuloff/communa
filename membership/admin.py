from django.contrib import admin

from .models import Membership


class MembershipAdmin(admin.ModelAdmin):
    fields = ("role", "apartment_number", "can_vote", "member", "organization")
    list_display = ("member", "organization", "role")
    list_filter = ("role", "organization")
    list_per_page = 50
    sortable_by = ("registered_at", "organization",)


admin.site.register(Membership, MembershipAdmin)
