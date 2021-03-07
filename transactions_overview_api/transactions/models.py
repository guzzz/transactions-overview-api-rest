from django.db import models

from .choices import TRANSACTION_TYPE_CHOICES


class Transaction(models.Model):
    reference = models.CharField(primary_key=True, max_length=6)
    account = models.CharField(max_length=6)
    date = models.DateField(null=False)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(
        to='users.CustomerUser',
        related_name='%(class)s',
        null=False,
        on_delete=models.CASCADE
    ) 

    def __str__(self):
        return self.reference
