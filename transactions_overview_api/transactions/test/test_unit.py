from django.db.utils import IntegrityError
from django.test import TestCase
from datetime import datetime

from transactions_overview_api.users.models import CustomerUser

from ..models import Transaction


class TransactionUnitTest(TestCase):
	@classmethod
	def setUpClass(cls):
		super(TransactionUnitTest, cls).setUpClass()
		print('======================================================================')
		print('==> INITIALIZING Transaction UNIT Tests...')
		print('======================================================================')
		print('... CREATING initial Transactions ..............................')
		
		user_instance = CustomerUser.objects.create(name="Thiago Neves", email="falazeze@bomdia.com", age=20)
		transaction = Transaction.objects.create(
			reference="000051",
			account="S00099",
			date=datetime.now().date(),
			amount="-51.13",
			type="outflow",
			category="groceries", 
			user=user_instance
		)

		print('----------------------------------------------------------------------')

	def test_create_existing_transaction(self):
		print('==> Creating EXISTING transaction')
		try:
			repeted_transaction = Transaction.objects.create(
				reference="000051",
				account="S00099",
				date=datetime.now().date(),
				amount="-51.13",
				type="outflow",
				category="groceries", 
				user=CustomerUser.objects.all().first()
			)
			self.assertEqual(False, True)
		except IntegrityError as error:
			self.assertEqual(error.args[0], 'duplicate key value violates unique constraint "transactions_transaction_pkey"\nDETAIL:  Key (reference)=(000051) already exists.\n')
		print('----------------------------------------------------------------------')

	def test_create_new_transaction(self):
		print('==> Creating NEW transaction')
		try:
			new_transaction = Transaction.objects.create(
				reference="000052",
				account="S00099",
				date=datetime.now().date(),
				amount="100.00",
				type="inflow",
				category="salary", 
				user=CustomerUser.objects.all().first()
			)
			self.assertEqual(type(new_transaction), Transaction)
		except:
			self.assertEqual(False, True)
		print('----------------------------------------------------------------------')

	def test_transaction_model(self):
		print('==> Testing MODEL')
		first_transaction = Transaction.objects.get(reference='000051')
		self.assertEqual(str(first_transaction), "000051")
		print('----------------------------------------------------------------------')
