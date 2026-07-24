from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from organization.models import Organization
from membership.models import Membership
from news.models import Post


class PostAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112233"
        )

        login = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email": "user@test.com",
                "password": "password123"
            }
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
        )

        self.organization = Organization.objects.create(
            name="Test Organization",
            city="Kyiv",
            street_address="Main street 12",
            post_index="02000"
        )

        Membership.objects.create(
            member=self.user,
            organization=self.organization,
            apartment_number=1,
            role=Membership.MemberRole.HEAD
        )

        self.url = reverse("post-list")

    def test_create_post(self):
        payload = {
            "title": "First news",
            "content": "Hello world",
            "organization": self.organization.id
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()

        self.assertEqual(post.title, "First news")
        self.assertEqual(post.content, "Hello world")
        self.assertEqual(post.organization, self.organization)

    def test_create_post_without_title(self):
        payload = {
            "content": "Hello",
            "organization": self.organization.id
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_without_organization(self):
        payload = {
            "title": "Hello",
            "content": "World"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_posts(self):
        Post.objects.create(
            title="Post 1",
            content="Content",
            organization=self.organization
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_post(self):
        post = Post.objects.create(
            title="Post",
            content="Content",
            organization=self.organization
        )

        response = self.client.get(
            reverse("post-detail", args=[post.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Post")

    def test_update_post(self):
        post = Post.objects.create(
            title="Old",
            content="Old content",
            organization=self.organization
        )

        payload = {
            "title": "New",
            "content": "New content",
            "organization": self.organization.id
        }

        response = self.client.put(
            reverse("post-detail", args=[post.id]),
            payload
        )

        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.title, "New")

    def test_partial_update_post(self):
        post = Post.objects.create(
            title="Old",
            content="Content",
            organization=self.organization
        )

        response = self.client.patch(
            reverse("post-detail", args=[post.id]),
            {
                "title": "Updated"
            }
        )

        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.title, "Updated")
        self.assertEqual(post.content, "Content")

    def test_delete_post(self):
        post = Post.objects.create(
            title="Delete",
            content="Content",
            organization=self.organization
        )

        response = self.client.delete(
            reverse("post-detail", args=[post.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_not_found(self):
        response = self.client.get(
            reverse("post-detail", args=[uuid4()])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_create_post(self):
        self.client.credentials()

        payload = {
            "title": "Post",
            "content": "Content",
            "organization": self.organization.id
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_post(self):
        post = Post.objects.create(
            title="Old",
            content="Content",
            organization=self.organization
        )

        self.client.credentials()

        response = self.client.patch(
            reverse("post-detail", args=[post.id]),
            {
                "title": "New"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_post(self):
        post = Post.objects.create(
            title="Delete",
            content="Content",
            organization=self.organization
        )

        self.client.credentials()

        response = self.client.delete(
            reverse("post-detail", args=[post.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
