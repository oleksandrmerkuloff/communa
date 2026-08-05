from rest_framework.viewsets import ModelViewSet

from .models import Budget, Income, Expense, Category
from .serializers import (
    BudgetWriterSerializer, BudgetReaderSerializer,
    IncomeWriterSerializer, IncomeReaderSerializer,
    ExpenseWriterSerializer, ExpenseReaderSerializer,
    CategorySerializer, CategoryShortSerializer
)
from .permissions import (
    CanCreateBudget, CanEditBudget, CanViewBudget, CanDeleteBudget,
    CanCreateCategory, CanDeleteCategory, CanEditCategory, CanViewCategory,
    CanEditIncome, CanViewIncome, CanCreateIncome, CanDeleteIncome,
    CanEditExpense, CanViewExpense, CanCreateExpense, CanDeleteExpense
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = [CanViewCategory]
        elif self.action == "create":
            self.permission_classes = [CanCreateCategory]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditCategory]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteCategory]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

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
        if self.action in ("list", "retrieve"):
            self.permission_classes = [CanViewBudget]
        elif self.action == "create":
            self.permission_classes = [CanCreateBudget]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditBudget]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteBudget]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

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
        if self.action in ("list", "retrieve"):
            self.permission_classes = [CanViewIncome]
        elif self.action == "create":
            self.permission_classes = [CanCreateIncome]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditIncome]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteIncome]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

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
        if self.action in ("list", "retrieve"):
            self.permission_classes = [CanViewExpense]
        elif self.action == "create":
            self.permission_classes = [CanCreateExpense]
        elif self.action in ("update", "partial_update"):
            self.permission_classes = [CanEditExpense]
        elif self.action == "destroy":
            self.permission_classes = [CanDeleteExpense]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

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
