from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from currency.models import Currency

class Command(BaseCommand):
    help = 'Generate 100 currencies with majority having is_crypto set to True'

    def handle(self, *args, **kwargs):
        num_crypto_currencies = 80  # Adjust as needed
        num_fiat_currencies = 20  # Adjust as needed

        for i in range(num_crypto_currencies):
            name = f"CryptoCurrency {i+1}"
            symbol = f"CC{i+1}"
            Currency.objects.create(
                name=name,
                symbol=symbol,
                is_crypto=True
            )

        for i in range(num_fiat_currencies):
            name = f"FiatCurrency {i+1}"
            symbol = f"FC{i+1}"
            Currency.objects.create(
                name=name,
                symbol=symbol,
                is_crypto=False
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated currencies'))
