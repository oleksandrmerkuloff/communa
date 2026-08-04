from django.contrib import admin

from .models import Budget, Category, AccountingAttachment, Expense, Income


class AccountingAttachmentInline(admin.TabularInline):
    model = AccountingAttachment
    extra = 1


class ExpenseAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["organization", "category", "amount", "date"]
    list_display_links = ["organization"]
    list_filter = ["organization", "category"]
    list_per_page = 50
    readonly_fields = ["created_at", "updated_at"]
    sortable_by = ["date", "created_at", "updated_at"]
    search_fields = ["organization__name", "category__name"]
    inlines = [AccountingAttachmentInline]


class IncomeAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["organization", "category", "amount", "date"]
    list_display_links = ["organization"]
    list_filter = ["organization", "category"]
    list_per_page = 50
    readonly_fields = ["created_at", "updated_at"]
    sortable_by = ["date", "created_at", "updated_at"]
    search_fields = ["organization__name", "category__name"]
    inlines = [AccountingAttachmentInline]


class BudgetAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["organization", "category", "month", "year"]
    list_display_links = ["organization"]
    list_filter = ["organization", "category", "year"]
    list_per_page = 50
    readonly_fields = ["created_at", "updated_at"]
    sortable_by = ["created_at", "updated_at", "year", "month"]
    search_fields = ["organization__name", "category__name"]
    inlines = [AccountingAttachmentInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "organization"]
    list_filter = ["organization"]
    search_fields = ["name", "organization__name"]


admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(AccountingAttachment)