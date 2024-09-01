from django.test import TestCase
from .models import Category, Discount, Product, ProductImages, ProductRate
from vendors.models import *

class ModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='test category')
        self.manager = Managers.objects.create(first_name="Test Customer", last_name="Test Customer",
                                               email="test1@gmail.com", phone='123451', password='test12345')
        self.store = Store.objects.create(name='test1', description='this is test', owner=self.manager)
        self.discount = Discount.objects.create(discount_type=Discount.DiscountType.cash, value=10)
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            quantity_in_stock=100,
            price=1000,
            discount=self.discount,
            category=self.category,
            store=self.store
        )
        self.product_image = ProductImages.objects.create(product=self.product, product_image="path/to/image.jpg")
        self.product_rate = ProductRate.objects.create(product=self.product, rate=5)

    def test_category_creation(self):
        self.assertEqual(self.category.title, "test category")


    def test_discount_creation(self):
        self.assertEqual(self.discount.discount_type, Discount.DiscountType.cash)
        self.assertEqual(self.discount.value, 10)

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "Test Description")
        self.assertEqual(self.product.quantity_in_stock, 100)
        self.assertEqual(self.product.price, 1000)
        self.assertEqual(self.product.discount, self.discount)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.store, self.store)

    def test_product_images_creation(self):
        self.assertEqual(self.product_image.product, self.product)
        self.assertEqual(self.product_image.product_image, "path/to/image.jpg")

    def test_product_rate_creation(self):
        self.assertEqual(self.product_rate.product, self.product)
        self.assertEqual(self.product_rate.rate, 5)




