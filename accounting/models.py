import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from organization.models import Organization


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(Organization, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "organization"],
                name="unique_organization_accounting_category_constraint"
            ),
        ]


class AccountingAttachment(TimestampMixin):
    file = models.FileField(upload_to="accounting/%Y/%m/")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()

    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"])
        ]


class Income(TimestampMixin):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, related_name="incomes", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="incomes")
    attachments = GenericRelation(AccountingAttachment, related_query_name="income")

    def __str__(self):
        return f"{self.amount} ({self.date})"

    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"
        ordering = ["-date", "-created_at"]
        indexes = [
                    models.Index(fields=["organization", "date"]),
                ]


class Expense(TimestampMixin):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    organization = models.ForeignKey(Organization, related_name="expenses", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    attachments = GenericRelation(AccountingAttachment, related_query_name="expense")

    def __str__(self):
        return f"{self.amount} ({self.date})"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-date", "-created_at"]
        indexes = [
                    models.Index(fields=["organization", "date"]),
                ]


class Budget(TimestampMixin):
    class MonthChoices(models.IntegerChoices):
        JANUARY = 1, 'January'
        FEBRUARY = 2, 'February'
        MARCH = 3, 'March'
        APRIL = 4, 'April'
        MAY = 5, 'May'
        JUNE = 6, 'June'
        JULY = 7, 'July'
        AUGUST = 8, 'August'
        SEPTEMBER = 9, 'September'
        OCTOBER = 10, 'October'
        NOVEMBER = 11, 'November'
        DECEMBER = 12, 'December'

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    organization = models.ForeignKey(Organization, related_name="budgets", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="budgets")
    planned_amount = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.PositiveSmallIntegerField()
    month = models.IntegerField(choices=MonthChoices.choices)
    attachments = GenericRelation(AccountingAttachment)

    def __str__(self):
        return f"{self.month}/{self.year} - {self.planned_amount}"

    class Meta:
            verbose_name = "Budget"
            verbose_name_plural = "Budgets"
            ordering = ["-year", "-month"]
            constraints = [
                        models.UniqueConstraint(
                            fields=["organization", "category", "year", "month"],
                            name="unique_budget_period_constraint"
                        ),
                    ]
            indexes = [
                        models.Index(fields=["organization", "year", "month"]),
                    ]
