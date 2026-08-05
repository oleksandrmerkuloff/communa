from uuid import uuid4
from decimal import Decimal
from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from organization.models import Organization
from membership.models import Membership
from accounting.models import Income, Category


class IncomeAPITest(APITestCase):
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

        self.url = reverse("income-list")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_income(self):
        payload = {
            "organization": str(self.organization.id),
            "category": str(self.category.id),
            "amount": 123.12,
            "date": "2026-09-20"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 1)
        income = Income.objects.first()
        self.assertEqual(income.category, self.category)
        self.assertEqual(income.amount, Decimal("123.12"))
        self.assertEqual(income.organization, self.organization)

    def test_create_income_without_organization(self):
        payload = {
            "category": str(self.category.id),
            "amount": 123.12,
            "date": "2026-09-20"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_incomes(self):
        Income.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_income(self):
        income = Income.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.get(
            reverse("income-detail", args=[income.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "123.12")
        self.assertEqual(response.data["date"], "2026-08-15")

    def test_partial_update_income(self):
        income = Income.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.patch(
            reverse("income-detail", args=[income.id]),
            {
                "amount": 111111.11
            }
        )   

        income.refresh_from_db()  

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(income.amount, Decimal("111111.11"))
        self.assertEqual(income.organization, self.organization)

    def test_delete_income(self):
        income = Income.objects.create(
            organization=self.organization,
            category=self.category,
            amount=123.12,
            date=date(2026, 8, 15)
        )

        response = self.client.delete(
            reverse("income-detail", args=[income.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Income.objects.count(), 0)
    