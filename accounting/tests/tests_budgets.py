from uuid import uuid4
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from organization.models import Organization
from membership.models import Membership
from accounting.models import Budget, Category


class BudgetAPITest(APITestCase):
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

        self.url = reverse("budget-list")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_budget(self):
        payload = {
            "organization": str(self.organization.id),
            "category": str(self.category.id),
            "planned_amount": 123.12,
            "year": 2026,
            "month": 2
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 1)
        budget = Budget.objects.first()
        self.assertEqual(budget.category, self.category)
        self.assertEqual(budget.year, 2026)
        self.assertEqual(budget.organization, self.organization)

    def test_create_budget_without_organization(self):
        payload = {
            "category": str(self.category.id),
            "planned_amount": 123.12,
            "year": 2026,
            "month": 2
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_budgets(self):
        Budget.objects.create(
            organization=self.organization,
            category=self.category,
            planned_amount=123.12,
            year=2026,
            month=2
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_budget(self):
        budget = Budget.objects.create(
            organization=self.organization,
            category=self.category,
            planned_amount=123.12,
            year=2026,
            month=2
        )

        response = self.client.get(
            reverse("budget-detail", args=[budget.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["planned_amount"], "123.12")
        self.assertEqual(response.data["year"], 2026)

    def test_partial_update_budget(self):
        budget = Budget.objects.create(
                organization=self.organization,
                category=self.category,
                planned_amount=123.12,
                year=2026,
                month=2
            )

        response = self.client.patch(
            reverse("budget-detail", args=[budget.id]),
            {
                "planned_amount": 111111.11
            }
        )   

        budget.refresh_from_db()  

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(budget.planned_amount, Decimal("111111.11"))
        self.assertEqual(budget.year, 2026)

    def test_delete_budget(self):
        budget = Budget.objects.create(
            organization=self.organization,
            category=self.category,
            planned_amount=123.12,
            year=2026,
            month=2
        )

        response = self.client.delete(
            reverse("budget-detail", args=[budget.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Budget.objects.count(), 0)
    