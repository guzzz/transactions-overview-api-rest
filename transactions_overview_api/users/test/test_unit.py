from django.db.utils import IntegrityError
from django.test import TestCase

from ..models import CustomerUser


class UserUnitTest(TestCase):
	@classmethod
	def setUpClass(cls):
		super(UserUnitTest, cls).setUpClass()
		print('======================================================================')
		print('==> INITIALIZING Users UNIT Tests...')
		print('======================================================================')
		print('... CREATING initial Users ..............................')
		
		initial_user = CustomerUser.objects.create(name="Adriano Imperador", email="adriano@email.com", age=20)

		print('----------------------------------------------------------------------')

	def test_create_existing_user(self):
		print('==> Creating EXISTING user')
		try:
			adriano_user = CustomerUser.objects.create(name="Adriano Imperador" ,email="adriano@email.com", age=20)
			self.assertEqual(False, True)
		except IntegrityError as error:
			self.assertEqual(error.args[0], 'duplicate key value violates unique constraint "users_customeruser_email_key"\nDETAIL:  Key (email)=(adriano@email.com) already exists.\n')
		print('----------------------------------------------------------------------')

	def test_create_new_user(self):
		print('==> Creating NEW user')
		try:
			ronaldinho_user = CustomerUser.objects.create(name="Ronaldinho Gaúcho", email="r10@email.com", age=20)
			self.assertEqual(type(ronaldinho_user), CustomerUser)
		except:
			self.assertEqual(False, True)
		print('----------------------------------------------------------------------')

	def test_custom_users_model(self):
		print('==> Testing MODEL')
		first_user = CustomerUser.objects.get(email='adriano@email.com')
		self.assertEqual(str(first_user), "Client: Adriano Imperador / Email: adriano@email.com / Age: 20")
		print('----------------------------------------------------------------------')
