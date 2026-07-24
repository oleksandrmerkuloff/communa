from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User


class JWTTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112233"
        )

        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email":"user@test.com",
                "password":"password123"
            }
        )

        self.access = response.data["access"]
        self.refresh = response.data["refresh"]

    def test_refresh(self):
        response = self.client.post(
            reverse("token_refresh"),
            {
                "refresh":self.refresh
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access",response.data)

    def test_logout(self):
        response = self.client.post(
            reverse("token_blacklist"),
            {
                "refresh":self.refresh
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_blacklisted_token(self):

        self.client.post(
            reverse("token_blacklist"),
            {
                "refresh":self.refresh
            }
        )

        response = self.client.post(
            reverse("token_refresh"),
            {
                "refresh":self.refresh
            }
        )

        self.assertEqual(response.status_code,401)
