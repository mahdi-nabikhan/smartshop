from django.test import TestCase
from .models import Customer, Address, Comments, Product

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
        self.product = Product.objects.create(name='Sample Product',quantity_in_stock=12,price=20,category_id=1,store_id=2)
        self.comment = Comments.objects.create(descriptions='Great product!', user=self.customer, product=self.product)

    def test_comment_creation(self):
        self.assertEqual(self.comment.descriptions, 'Great product!')
        self.assertEqual(self.comment.user, self.customer)
        self.assertEqual(self.comment.product, self.product)
        self.assertEqual(self.comment.status, Comments.Status.pending)
