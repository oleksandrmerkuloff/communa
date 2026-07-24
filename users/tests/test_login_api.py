from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class LoginTest(APITestCase):

    def setUp(self):
        self.url = reverse("token_obtain_pair")

        User.objects.create_user(
            email="user@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112233"
        )

    def test_login(self):
        response = self.client.post(self.url,{
            "email":"user@test.com",
            "password":"password123"
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn("access",response.data)
        self.assertIn("refresh",response.data)

    def test_wrong_password(self):
        response = self.client.post(self.url,{
            "email":"user@test.com",
            "password":"wrong"
        })

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_wrong_email(self):
        response = self.client.post(self.url,{
            "email":"wrong@test.com",
            "password":"password123"
        })

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)