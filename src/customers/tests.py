from django.test import TestCase

from website.models import Category
from .models import Customer, Address, Comments, Product
from vendors.models import *

class CustomerModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create_user(email='customer@example.com', password='password123')

    def test_create_customer(self):
        self.assertTrue(self.customer.is_customer)
        self.assertEqual(self.customer.email, 'customer@example.com')

class AddressModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create_user(email='customer@example.com', password='password123')
        self.address = Address.objects.create(country='Iran', city='Qazvin', street='Main St', user=self.customer)

    def test_address_creation(self):
        self.assertEqual(self.address.country, 'Iran')
        self.assertEqual(self.address.city, 'Qazvin')
        self.assertEqual(self.address.street, 'Main St')
        self.assertEqual(self.address.user, self.customer)

class CommentsModelTest(TestCase):

    def setUp(self):

        self.customer = Customer.objects.create_user(email='customer@example.com', password='password123')
        self.category = Category.objects.create(title='test category')
        self.manager = Managers.objects.create(first_name="Test Customer", last_name="Test Customer",
                                               email="test1@gmail.com", phone='123451', password='test12345')
        self.store = Store.objects.create(name='test1', description='this is test', owner=self.manager)

        self.product = Product.objects.create(name='Sample Product',quantity_in_stock=12,price=20,category=self.category,store=self.store)
        self.comment = Comments.objects.create(descriptions='Great product!', user=self.customer, product=self.product)

    def test_comment_creation(self):
        self.assertEqual(self.comment.descriptions, 'Great product!')
        self.assertEqual(self.comment.user, self.customer)
        self.assertEqual(self.comment.product, self.product)
        self.assertEqual(self.comment.status, Comments.Status.pending)



from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import RegisterForm

class CustomerRegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('customers:customer_register')
        self.User = get_user_model()

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/register.html')

    def test_register_post_valid(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
        }
        response = self.client.post(self.register_url, form_data)
        self.assertEqual(response.status_code, 200)


