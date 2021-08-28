import json

from django.test import TestCase, Client
from rest_framework import status
from vending_machine.models import User, Product


class BuyProdutApiTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.buyer = User.objects.create(
            username='casper', first_name='Casper', last_name='Houghan', password=1234, role='buyer', deposit=100)
        self.seller = User.objects.create(
            username='vimox', first_name='Vimox', last_name='Shah', password=1234, role='seller', deposit=0)

        self.valid_payload = {
            'deposit': 100
        }
        self.invalid_payload = {
            'deposit': 15
        }



    def test_user_deposit(self):
        self.client.force_login(self.seller)
        response = self.client.post(
            'http://localhost:8000/user/deposit',
            data=self.valid_payload,
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(json.loads(response.content)['errors'][0]['message'],
                         'Only buyer is allowed')

        self.client.force_login(self.buyer)
        response = self.client.post(
            'http://localhost:8000/user/deposit',
            data=self.invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(json.loads(response.content)['errors'][0]['message'],
                         'you can only deposit 5,10,20,50,100 cents')

        self.client.force_login(self.buyer)
        response = self.client.post(
            'http://localhost:8000/user/deposit',
            data=self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_reset_deposit(self):
        self.client.force_login(self.seller)
        response = self.client.put(
            'http://localhost:8000/user/reset_deposit',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(json.loads(response.content)['errors'][0]['message'],
                         'Only buyer is allowed')

        self.client.force_login(self.buyer)
        response = self.client.put(
            'http://localhost:8000/user/reset_deposit',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['data']['deposit'], 0)