from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order


# Create your tests here.

class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='testuser', password='123')
        permission = Permission.objects.get(
            codename='view_order',
            content_type__app_label='shopapp'
        )
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='test address',
            promocode='123',
            user=self.user
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:orders_details', kwargs={'pk': self.order.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.order)
        self.assertContains(response, self.order.promocode)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'products-fixtures.json',
        'orders-fixtures.json',
        'users-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='testuser', password='123', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_export(self):
        response = self.client.get(
            reverse('shopapp:orders_export')
        )
        orders = Order.objects.select_related("user").prefetch_related("products").all()
        self.assertEqual(response.status_code, 200)
        for order, order_res in zip(orders, response):
            self.assertContains(order, order_res)
