from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type_choices = [
        ('trade', 'Trade'),
        ('swap', 'Swap'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        # Add more transaction types as needed
    ]
    transaction_type = models.CharField(max_length=20, choices=transaction_type_choices)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add more fields specific to each transaction type as needed

    def __str__(self):
        return f'{self.user.username} - {self.transaction_type} - {self.amount} {self.currency}'
