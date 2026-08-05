from uuid import uuid4
from decimal import Decimal
from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from organization.models import Organization
from membership.models import Membership
from accounting.models import Expense, Category


class ExpenseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="head@test.com",
            phone_number="+380501112233",
            first_name="Head",
            last_name="User",
            password="password123"
        )

        self.organization = Organization.objects.create(
            name="OSBB",
            city="Kyiv",
            street_address="Main street",
            post_index="01001"
        )

        self.category = Category.objects.create(
            name="First and Test",
            organization=self.organization
        )

        Membership.objects.create(
            apartment_number=13,
            member=self.user,
            organization=self.organization,
            role=Membership.MemberRole.HEAD
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "email": "head@test.com",
                "password": "password123"
            }
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )

        self.url = reverse("expense-list")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_expense(self):
        payload = {
            "organization": str(self.organization.id),
            "category": str(self.category.id),
            "amount": 123.12,
            "date": "2026-09-20"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        self.assertEqual(expense.category, self.category)
        self.assertEqual(expense.amount, Decimal("123.12"))
        self.assertEqual(expense.organization, self.organization)

    def test_create_expense_without_organization(self):
        payload = {
            "category": str(self.category.id),
            "amount": 123.12,
            "date": "2026-09-20"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_expenses(self):
        Expense.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_expense(self):
        expense = Expense.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.get(
            reverse("expense-detail", args=[expense.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "123.12")
        self.assertEqual(response.data["date"], "2026-08-15")

    def test_partial_update_expense(self):
        expense = Expense.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.patch(
            reverse("expense-detail", args=[expense.id]),
            {
                "amount": 111111.11
            }
        )   

        expense.refresh_from_db()  

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expense.amount, Decimal("111111.11"))
        self.assertEqual(expense.organization, self.organization)

    def test_delete_expense(self):
        expense = Expense.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.delete(
            reverse("expense-detail", args=[expense.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)
