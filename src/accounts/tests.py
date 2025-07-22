from django.test import TestCase
from .models import User, Codes
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from vendors.models import Managers, Admin, Operator
from customers.models import *
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from vendors.models import Managers, Admin, Operator, Store


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


class LoginViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')  # فرض کنید نام URL برای این ویو 'login' است
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpassword')
        self.manager = Managers.objects.create(first_name="Test Customer", last_name="Test Customer",
                                               email="test1@gmail.com", phone='123451', password='test12345')
        self.store = Store.objects.create(name='test1', description='this is test', owner=self.manager)
        Managers.objects.create(first_name="Test Manager", last_name="Test Manager", email="test37@gmail.com",
                                phone='1234513')
        Admin.objects.create(first_name='Test Admin', last_name='Test Admin', email='test67@gmail.com', phone='123456',
                             password='<PASSWORD>', store=self.store)
        Operator.objects.create(first_name="Test Operator", last_name="Test Operator", email="test12@gmail.com",
                                phone='1234518', password='<PASSWORD>', store=self.store)
        Customer.objects.create(first_name="Test Customer", last_name="Test Customer", email="test19@gmail.com",
                                phone='12345112', password='1234567')

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.equal = self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/login.html')

    def test_login_redirect_manager(self):
        response = self.client.post(self.login_url, {'email': 'test@example.com', 'password': 'testpassword'})
        self.equal = self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dashboards:admin_panel'))

    def test_login_redirect_customer(self):
        self.delete = Managers.objects.filter(id=self.user.id).delete()
        Admin.objects.filter(id=self.user.id).delete()
        Operator.objects.filter(id=self.user.id).delete()
        response = self.client.post(self.login_url, {'email': 'test@example.com', 'password': 'testpassword'})
        self.equal = self.assertEqual(response.status_code, 200)
        print(response.content)
        self.assertRedirects(response, reverse('website:landing_page'))
