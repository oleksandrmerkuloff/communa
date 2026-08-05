from rest_framework import routers

from .views import CategoryViewSet, BudgetViewSet, IncomeViewSet, ExpenseViewSet


router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'budgets', BudgetViewSet, basename="budget")
router.register(r'incomes', IncomeViewSet, basename="income")
router.register(r'expenses', ExpenseViewSet, basename="expense")

urlpatterns = router.urls
