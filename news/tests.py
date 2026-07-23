from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from organization.models import Organization
from membership.models import Membership
from .models import Tag


class TagAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="head.test.com",
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

    def test_create_tag(self):
        response = self.client.post(
            "/api/news/tags/",
            {
                "name": "Important",
                "organization": str(self.organization.id)
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, "Important")

    def test_list_tags(self):
        Tag.objects.create(
            name="Finance",
            organization=self.organization
        )

        response = self.client.get("/api/news/tags/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_tag(self):
        tag = Tag.objects.create(
            name="Finance",
            organization=self.organization
        )

        response = self.client.patch(
            f"/api/news/tags/{tag.id}/",
            {
                "name": "Updated"
            }
        )

        tag.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, "Updated")

    def test_delete_tag(self):
        tag = Tag.objects.create(
            name="Finance",
            organization=self.organization
        )

        response = self.client.delete(
            f"/api/news/tags/{tag.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())


# class TagPermissionTest(APITestCase):
#     pass
