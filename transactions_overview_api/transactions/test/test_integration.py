import json
from rest_framework.test import APITestCase
from datetime import datetime

from transactions_overview_api.users.models import CustomerUser

from ..models import Transaction
from .requests import *


class TransactionTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(TransactionTest, cls).setUpClass()
        print('======================================================================')
        print('==> INITIALIZING Transactions INTEGRATION Tests...')
        print('======================================================================')
        print('... CREATING initial Transactions ..............................')
        
        user_instance = CustomerUser.objects.create(name="Zlatan Ibrahimović", email="ibra@email.com", age=20)

        transaction_1 = Transaction.objects.create(
            reference="111111",
            account="S00099",
            date=datetime.now().date(),
            amount="-51.13",
            type="outflow",
            category="groceries", 
            user=user_instance
        )
        transaction_2 = Transaction.objects.create(
            reference="000052",
            account="S00099",
            date=datetime.now().date(),
            amount="100.12",
            type="inflow",
            category="salary", 
            user=user_instance
        )
        transaction_3 = Transaction.objects.create(
            reference="000053",
            account="C00100",
            date=datetime.now().date(),
            amount="2000.56",
            type="inflow",
            category="savings", 
            user=user_instance
        )
        print('----------------------------------------------------------------------')

    def test_list_transactions(self):
        print('==> LIST: [GET] /transactions/')
        response = self.client.get('/transactions/')
        self.assertEqual(response.status_code, 200)
        print('----------------------------------------------------------------------')

    def test_create_transaction(self):
        print('==> CREATE: [POST] /transactions/')
        data = {
            "reference":"110999",
            "account":"SSS000",
            "date":"2020-01-10",
            "amount":"150.72",
            "type":"inflow",
            "category":"savings",
            "user_id":1
        }
        response = self.client.post('/transactions/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "reference":"110999",
            "account":"SSS000",
            "date":"2020-01-10",
            "amount":"150.72",
            "type":"inflow",
            "category":"savings"
        })
        print('----------------------------------------------------------------------')

    def test_retrieve_summary_by_account(self):
        print('==> RETRIEVE: [GET] /summary-accounts/1/ ')
        response = self.client.get('/summary-accounts/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,[
            {
                'account': 'C00100', 'balance': '2000.56', 'total_inflow': '2000.56', 'total_outflow': '0'
            }, 
            {
                'account': 'S00099', 'balance': '48.99', 'total_inflow': '100.12', 'total_outflow': '-51.13'
            }
        ])
        print('----------------------------------------------------------------------')

    def test_retrieve_summary_by_categories(self):
        print('==> RETRIEVE: [GET] /summary-categories/1/ ')
        response = self.client.get('/summary-categories/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'inflow': {'salary': '100.12', 'savings': '2000.56'}, 'outflow': {'groceries': '-51.13'}})
        print('----------------------------------------------------------------------')

    def test_bulk_create_transaction(self):
        print('==> BULK CREATE: [POST] /transactions/')
        response = self.client.post('/transactions/', data=json.dumps(INPUT_MANY_TRANSACTIONS_1), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        print('----------------------------------------------------------------------')

    def test_bulk_force_create_transaction(self):
        print('==> FORCE BULK CREATE: [POST] /force-bulk-transactions/')
        response = self.client.post('/force-bulk-transactions/', data=json.dumps(INPUT_MANY_TRANSACTIONS_1), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        print('----------------------------------------------------------------------')


        ###############################################################################

        ################################ FAIL REQUESTS ################################

        ###############################################################################


    def test_create_same_reference_transaction(self):
        print('==> FAIL CREATE: [POST] /transactions/ (Same REFERENCE)')
        data = {
            "reference":"111111",
            "account":"S00012",
            "date":"2020-01-10",
            "amount":"150.72",
            "type":"inflow",
            "category":"savings",
            "user_id":1
        }
        response = self.client.post('/transactions/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        print('----------------------------------------------------------------------')


    def test_transaction_associated_to_unknown_user_id(self):
        print('==> FAIL CREATE: [POST] /transactions/ (UNKNOWN user_id)')
        data = {
            "reference":"999001",
            "account":"S00012",
            "date":"2020-01-10",
            "amount":"150.72",
            "type":"inflow",
            "category":"savings",
            "user_id":2
        }
        response = self.client.post('/transactions/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)


    def test_retrieve_summary_by_account_unknown_user_id(self):
        print('==> FAIL RETRIEVE: [GET] /summary-accounts/2/ (UNKNOWN user_id)')
        response = self.client.get('/summary-accounts/2/')
        self.assertEqual(response.status_code, 404)
        print('----------------------------------------------------------------------')

    def test_retrieve_summary_by_categories_unknown_user_id(self):
        print('==> FAIL RETRIEVE: [GET] /summary-categories/2/ (UNKNOWN user_id)')
        response = self.client.get('/summary-categories/2/')
        self.assertEqual(response.status_code, 404)
        print('----------------------------------------------------------------------')

    def test_fail_bulk_create_transaction(self):
        print('==> FAIL BULK CREATE: [POST] /transactions/')
        response = self.client.post('/transactions/', data=json.dumps(INPUT_MANY_TRANSACTIONS_2_FAIL), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        print('----------------------------------------------------------------------')
    
    def test_partial_fail_bulk_create_transaction(self):
        print('==> PARTIAL FAIL BULK CREATE: [POST] /transactions/')
        response = self.client.post('/transactions/', data=json.dumps(INPUT_MANY_TRANSACTIONS_3_FAIL), content_type="application/json")
        self.assertEqual(response.status_code, 207)
        print('----------------------------------------------------------------------')

    def test_fail_force_bulk_create_transaction(self):
        print('==> FAIL FORCE BULK CREATE: [POST] /force-bulk-transactions/')
        response = self.client.post('/force-bulk-transactions/', data=json.dumps(INPUT_MANY_TRANSACTIONS_4_FAIL), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        print('----------------------------------------------------------------------')

    def test_partial_fail_force_bulk_create_transaction(self):
        print('==> FAIL FORCE BULK CREATE: [POST] /force-bulk-transactions/')
        response = self.client.post('/force-bulk-transactions/', data=json.dumps(INPUT_MANY_TRANSACTIONS_5_FAIL), content_type="application/json")
        self.assertEqual(response.status_code, 207)
        print('----------------------------------------------------------------------')
