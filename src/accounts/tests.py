from django.test import TestCase
from .models import User, Codes

class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')

    def test_create_user(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='admin@example.com', password='admin123')
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)

class CodesModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.code = Codes.objects.create(user=self.user)

    def test_code_creation(self):
        self.assertEqual(len(self.code.number), 5)
        self.assertTrue(self.code.number.isdigit())
