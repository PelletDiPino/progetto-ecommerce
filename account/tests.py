from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
# Create your tests here.


class AnonymousUserViewTest(TestCase):

    def test_cannot_access_account_info(self):
        response = self.client.get(reverse('account:account_details'))
        self.assertEqual(response.status_code, 302)

    

class CustomerViewTests(TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='pass')

    def login(self):
        login = self.client.login(username='test', password='pass')
        return login

    def test_login(self):
        self.assertEqual(self.login(), True)

    def test_can_access_account_view(self):
        self.login()
        response = self.client.get(reverse('account:account_details'))
        self.assertEqual(response.status_code, 200)

    def test_cannot_access_vendor_view(self):
        self.login()
        response = self.client.get(reverse('account:my_sales'))
        self.assertEqual(response.status_code, 403)

    def test_cannot_create_product(self):

        self.login()
        responses = [
            self.client.get(reverse('product:create_product')),
            self.client.post(reverse('product:create_product'))
        ]
        for response in responses:
            self.assertEqual(response.status_code, 403)


class VendorViewTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='pass')
        vendor_group = Group.objects.create(name='vendors')
        self.test_user.groups.add(vendor_group)

    def login(self):
        login = self.client.login(username='test', password='pass')
        return login

    def test_can_create_sale(self):
        self.login()
        responses = [
            self.client.get(reverse('product:create_product')),
            self.client.post(reverse('product:create_product'))
        ]
        for response in responses:
            self.assertEqual(response.status_code, 200)