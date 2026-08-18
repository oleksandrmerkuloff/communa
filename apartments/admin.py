from django.contrib import admin

from .models import Apartment, ApartmentMembership


class ApartmentAdmin(admin.ModelAdmin):
    fields = ("organization", "number",)
    list_display = ("organization", "number",)
    list_filter = ("organization",)
    list_per_page = 50
    sortable_by = ("organization",)


class ApartmentMembershipAdmin(admin.ModelAdmin):
    fields = ("apartment", "member", "role")
    list_display = ("apartment", "member", "role")
    list_filter = ("apartment", "role",)
    list_per_page = 50
    sortable_by = ("role",)


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentMembership, ApartmentMembershipAdmin)
