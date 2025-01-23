from django.core.management.base import BaseCommand
from django.utils import timezone
from trade.models import Trade

class Command(BaseCommand):
    help = 'Check trade statuses and update wallet balances'

    def handle(self, *args, **kwargs):
        # Get trades that are ongoing and have reached their end time
        completed_trades = Trade.objects.filter(trade_status='ongoing', end_time__lte=timezone.now())
        
        for trade in completed_trades:
            # Update trade status based on outcome
            if trade.trade_outcome == 'win_trades':
                trade.trade_status = 'won'
                # Update wallet balance if the trade is a win
                trade.wallet.balance += trade.expected_payout
                trade.wallet.save()
            else:
                trade.trade_status = 'lost'
            trade.save()

        self.stdout.write(self.style.SUCCESS('Successfully checked trade statuses and updated wallet balances.'))
