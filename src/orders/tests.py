from django.test import TestCase
from customers.models import Customer, Address
from website.models import Product
from .models import Cart, OrderDetail, Bill
from vendors.models import *
from website.models import *
class ModelsTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='test category')

        self.manager = Managers.objects.create(first_name="Test Customer", last_name="Test Customer",
                                                email="test1@gmail.com", phone='123451', password='test12345')
        self.store=Store.objects.create(name='test1',description='this is test',owner=self.manager)
        self.store_Address = StoreAddress.objects.create(country='1',city='2',street='9',store=self.store)
        self.customer = Customer.objects.create(first_name="Test Customer", last_name="Test Customer",
                                                email="test@gmail.com", phone='12345', password='test12345')
        self.address = Address.objects.create(user=self.customer, country='a', city='a', street='m')
        self.product = Product.objects.create(name="Test Product", price=100.00, quantity_in_stock=12, store=self.store,
                                              category=self.category)
        self.cart = Cart.objects.create(user=self.customer)
        self.order_detail = OrderDetail.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.bill = Bill.objects.create(cart=self.cart, address=self.address)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.customer)
        self.assertFalse(self.cart.status)

    def test_order_detail_creation(self):
        self.assertEqual(self.order_detail.cart, self.cart)
        self.assertEqual(self.order_detail.product, self.product)
        self.assertEqual(self.order_detail.quantity, 2)
        self.assertEqual(self.order_detail.total_price, 200.00)
        self.assertFalse(self.order_detail.processed)

    def test_bill_creation(self):
        self.assertEqual(self.bill.cart, self.cart)
        self.assertEqual(self.bill.address, self.address)
        self.assertFalse(self.bill.status)
