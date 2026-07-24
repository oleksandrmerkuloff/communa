from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User


class RegisterAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("user-list")

    def test_register(self):
        payload = {
            "email": "user@test.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+380991112233"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email="user@test.com",
            password="password123",
            first_name="Eva",
            last_name="Adams",
            phone_number="+380991112234"
        )

        payload = {
                    "email": "user@test.com",
                    "password": "password123",
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "+380991112233"
            }
        

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_phone(self):
        payload = {
            "email": "user@test.com",
            "password": "password123",
            "phone_number": "123"
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_hashed(self):
        payload = {
                    "email": "user@test.com",
                    "password": "password123",
                    "first_name": "John",
                    "last_name": "Doe",
                    "phone_number": "+380991112233"
            }
    
        self.client.post(self.url, payload)
    
        user = User.objects.get(email="user@test.com")
    
        self.assertNotEqual(user.password, "password123")
        self.assertTrue(user.check_password("password123"))
