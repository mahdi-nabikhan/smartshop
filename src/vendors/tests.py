from django.test import TestCase
from .models import Managers, Store, StoreRate, StoreAddress, Admin, Operator
from accounts.models import User


class ModelsTestCase(TestCase):

    def setUp(self):
        self.manager = Managers.objects.create(first_name='Manager', last_name='One', email='manager1@example.com',
                                               phone='1234556')
        self.store = Store.objects.create(name='Test Store', description='A test store', owner=self.manager)
        self.store_rate = StoreRate.objects.create(rate=5, store=self.store)
        self.store_address = StoreAddress.objects.create(country='Iran', city='Qazvin', street='Test Street',
                                                         store=self.store)
        self.admin = Admin.objects.create(first_name='Admin', last_name='One', email='admin1@example.com',
                                          store=self.store, phone='9978')
        self.operator = Operator.objects.create(first_name='Operator', last_name='One', email='operator1@example.com',
                                                store=self.store, phone='9988')

    def test_manager_creation(self):
        self.assertEqual(self.manager.first_name, 'Manager')
        self.assertTrue(self.manager.is_Managers)

    def test_store_creation(self):
        self.assertEqual(self.store.name, 'Test Store')
        self.assertEqual(self.store.owner, self.manager)

    def test_store_rate_creation(self):
        self.assertEqual(self.store_rate.rate, 5)
        self.assertEqual(self.store_rate.store, self.store)


    def test_store_address_creation(self):
        self.assertEqual(self.store_address.country, 'Iran')
        self.assertEqual(self.store_address.city, 'Qazvin')
        self.assertEqual(self.store_address.street, 'Test Street')
        self.assertEqual(self.store_address.store, self.store)

    def test_admin_creation(self):
        self.assertEqual(self.admin.first_name, 'Admin')
        self.assertTrue(self.admin.is_admins)
        self.assertEqual(self.admin.store, self.store)

    def test_operator_creation(self):
        self.assertEqual(self.operator.first_name, 'Operator')
        self.assertTrue(self.operator.is_operator)
        self.assertEqual(self.operator.store, self.store)
