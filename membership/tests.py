from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from organization.models import Organization
from membership.models import Membership


class MembershipAPITest(APITestCase):

    def setUp(self):
        self.head = User.objects.create_user(
            email="head@test.com",
            password="password123",
            first_name="Head",
            last_name="User",
            phone_number="+380991111111"
        )

        self.resident = User.objects.create_user(
            email="resident@test.com",
            password="password123",
            first_name="Resident",
            last_name="User",
            phone_number="+380992222222"
        )

        login = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email": "head@test.com",
                "password": "password123"
            }
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
        )

        self.organization = Organization.objects.create(
            name="Test Organization",
            city="Kyiv",
            street_address="Main Street 12",
            post_index="02000"
        )

        self.head_membership = Membership.objects.create(
            member=self.head,
            organization=self.organization,
            apartment_number=1,
            role=Membership.MemberRole.HEAD
        )

        self.url = reverse("membership-list")

    def test_head_can_add_resident(self):
        payload = {
            "member": self.resident.id,
            "organization": self.organization.id,
            "apartment_number": 25,
            "role": Membership.MemberRole.RESIDENT
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Membership.objects.count(), 2)

    def test_create_without_auth(self):
        self.client.credentials()

        payload = {
            "member": self.resident.id,
            "organization": self.organization.id,
            "apartment_number": 25,
            "role": Membership.MemberRole.RESIDENT
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_without_required_fields(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_members(self):
        Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_member(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        response = self.client.get(
            reverse("membership-detail", args=[member.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_not_found(self):
        response = self.client.get(
            reverse("membership-detail", args=[uuid4()])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_head_can_update_member(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        response = self.client.patch(
            reverse("membership-detail", args=[member.id]),
            {
                "apartment_number": 15
            }
        )

        member.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(member.apartment_number, 15)

    def test_partial_update_member(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        response = self.client.patch(
            reverse("membership-detail", args=[member.id]),
            {
                "role": Membership.MemberRole.HEAD
            }
        )

        member.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(member.role, Membership.MemberRole.HEAD)

    def test_unauthorized_update(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        self.client.credentials()

        response = self.client.patch(
            reverse("membership-detail", args=[member.id]),
            {
                "apartment_number": 100
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_head_can_delete_member(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        response = self.client.delete(
            reverse("membership-detail", args=[member.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Membership.objects.filter(id=member.id).exists()
        )

    def test_unauthorized_delete(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        self.client.credentials()

        response = self.client.delete(
            reverse("membership-detail", args=[member.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_created_member_has_resident_role(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        self.assertEqual(
            member.role,
            Membership.MemberRole.RESIDENT
        )

    def test_head_role_is_preserved(self):
        self.assertEqual(
            self.head_membership.role,
            Membership.MemberRole.HEAD
        )

    def test_head_can_change_member_role(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        self.client.patch(
            reverse("membership-detail", args=[member.id]),
            {
                "role": Membership.MemberRole.HEAD
            }
        )

        member.refresh_from_db()

        self.assertEqual(
            member.role,
            Membership.MemberRole.HEAD
        )

    def test_apartment_number_saved(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=42,
            role=Membership.MemberRole.RESIDENT
        )

        self.assertEqual(member.apartment_number, 42)

    def test_member_belongs_to_correct_organization(self):
        member = Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        self.assertEqual(
            member.organization,
            self.organization
        )

    def test_same_user_cannot_join_twice(self):
        Membership.objects.create(
            member=self.resident,
            organization=self.organization,
            apartment_number=5,
            role=Membership.MemberRole.RESIDENT
        )

        payload = {
            "member": self.resident.id,
            "organization": self.organization.id,
            "apartment_number": 15,
            "role": Membership.MemberRole.RESIDENT
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
