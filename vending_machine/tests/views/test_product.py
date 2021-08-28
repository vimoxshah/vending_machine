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
        self.product = Product.objects.create(amount_available=100,cost=5, product_name='bag', seller_id=self.seller.id)


        self.valid_payload = {
            'product_id': self.product.id,
            'amount': 5
        }
        self.invalid_payload = {
            'product_id': self.product.id,
            'amount': 110
        }

        self.invalid_payload_1 = {
            'product_id': self.product.id,
            'amount': 21
        }


    def test_buy_product(self):
        self.client.force_login(self.buyer)
        response = self.client.post(
            'http://localhost:8000/product/buy',
            data=self.valid_payload,
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_spent'], 25)
        self.assertEqual(response.data['change'], [50, 20, 5])

        self.client.force_login(self.seller)
        response = self.client.post(
            'http://localhost:8000/product/buy',
            data=self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(json.loads(response.content)['errors'][0]['message'], 'Only buyer is allowed')

        self.client.force_login(self.buyer)
        response = self.client.post(
            'http://localhost:8000/product/buy',
            data=self.invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        response = self.client.post(
            'http://localhost:8000/product/buy',
            data=self.invalid_payload_1,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(json.loads(response.content)['errors'][0]['message'],
                         'Total amount is more than you have deposited. please deposit more coins')


