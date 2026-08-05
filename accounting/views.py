from rest_framework.viewsets import ModelViewSet

from .models import Budget, Income, Expense, Category
from .serializers import (
    BudgetWriterSerializer, BudgetReaderSerializer,
    IncomeWriterSerializer, IncomeReaderSerializer,
    ExpenseWriterSerializer, ExpenseReaderSerializer,
    CategorySerializer, CategoryShortSerializer
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_permissions(self):
        pass

    def get_queryset(self):
        return (
            Category.objects
            .filter(organization__memberships__member=self.request.user)
            .select_related("organization")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CategoryShortSerializer
        return CategorySerializer


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all()

    def get_permissions(self):
        pass

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Budget.objects.none()

        return (
            Budget.objects
            .filter(organization__memberships__member=self.request.user)
            .select_related("organization", "category")
            .prefetch_related("attachments")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BudgetReaderSerializer
        return BudgetWriterSerializer


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all()

    def get_permissions(self):
        pass

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Income.objects.none()

        return (
            Income.objects
            .filter(organization__memberships__member=self.request.user)
            .select_related("organization", "category")
            .prefetch_related("attachments")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return IncomeReaderSerializer
        return IncomeWriterSerializer


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()

    def get_permissions(self):
        pass

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Expense.objects.none()

        return (
            Expense.objects
            .filter(organization__memberships__member=self.request.user)
            .select_related("organization", "category")
            .prefetch_related("attachments")
            .distinct()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ExpenseReaderSerializer
        return ExpenseWriterSerializer
