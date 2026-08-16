from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="user@test.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112233",
        )

        self.assertEqual(user.email, "user@test.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@test.com",
            password="password123",
            first_name="Eva",
            last_name="Adams",
            phone_number="+380991112234",
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_admin)

    def test_email_normalized(self):
        user = User.objects.create_user(
            email="TEST@MAIL.COM",
            password="password123",
            first_name="John",
            last_name="Doe",
            phone_number="+380991112233",
        )

        self.assertEqual(user.email, "TEST@mail.com")
