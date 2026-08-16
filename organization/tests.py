from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Organization
from users.models import User
from membership.models import Membership


class OrganizationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="head@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112233",
        )

        login = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "head@test.com", "password": "password123"},
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

        self.url = reverse("organization-list")

    def test_create_organization(self):
        payload = {
            "name": "Test Organization",
            "city": "Kyiv",
            "street_address": "Main Street 12",
            "post_index": "9060",
            "apartment_number": 11,
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Organization.objects.count(), 1)

    def test_creator_becomes_head(self):
        payload = {
            "name": "Test Organization",
            "city": "Kyiv",
            "street_address": "Main Street 12",
            "post_index": "9060",
            "apartment_number": 11,
        }

        self.client.post(self.url, payload)

        organization = Organization.objects.first()

        membership = Membership.objects.get(member=self.user, organization=organization)

        self.assertEqual(membership.role, Membership.MemberRole.HEAD)

    def test_apartment_saved(self):
        payload = {
            "name": "Test Organization",
            "city": "Kyiv",
            "street_address": "Main Street 12",
            "post_index": "9060",
            "apartment_number": 11,
        }
        self.client.post(self.url, payload)

        membership = Membership.objects.first()

        self.assertEqual(membership.apartment_number, 11)

    def test_list_organizations(self):

        organization = Organization.objects.create(
            name="Test Organization",
            city="Dnipro",
            street_address="Lozod 19a",
            post_index="1042",
        )

        Membership.objects.create(
            member=self.user,
            organization=organization,
            apartment_number=1,
            role=Membership.MemberRole.HEAD,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

    def test_retrieve_organization(self):

        organization = Organization.objects.create(
            name="Test Organization",
            city="Dnipro",
            street_address="Lozod 19a",
            post_index="1042",
        )

        Membership.objects.create(
            member=self.user,
            organization=organization,
            apartment_number=1,
            role=Membership.MemberRole.HEAD,
        )

        response = self.client.get(
            reverse("organization-detail", args=[organization.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_organization(self):

        organization = Organization.objects.create(
            name="Old Name",
            city="Dnipro",
            street_address="Lozod 19a",
            post_index="1042",
        )

        Membership.objects.create(
            member=self.user,
            organization=organization,
            role=Membership.MemberRole.HEAD,
            apartment_number=10,
        )

        response = self.client.patch(
            reverse("organization-detail", args=[organization.id]), {"name": "New Name"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization.refresh_from_db()

        self.assertEqual(organization.name, "New Name")

    def test_delete_organization(self):

        organization = Organization.objects.create(
            name="Delete me",
            city="Dnipro",
            street_address="Lozod 19a",
            post_index="1042",
        )

        Membership.objects.create(
            member=self.user,
            organization=organization,
            role=Membership.MemberRole.HEAD,
            apartment_number=10,
        )

        response = self.client.delete(
            reverse("organization-detail", args=[organization.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Organization.objects.filter(id=organization.id).exists())

    def test_anonymous_cannot_create(self):

        self.client.credentials()

        response = self.client.post(self.url, {"name": "Test"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_resident_cannot_update(self):

        resident = User.objects.create_user(
            email="resident@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112213",
        )

        organization = Organization.objects.create(
            name="Organization",
            city="Dnipro",
            street_address="Lozod 19a",
            post_index="1042",
        )

        Membership.objects.create(
            member=resident,
            organization=organization,
            role=Membership.MemberRole.RESIDENT,
            apartment_number=12,
        )

        login = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "resident@test.com", "password": "password123"},
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

        response = self.client.patch(
            reverse("organization-detail", args=[organization.id]), {"name": "New Name"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
