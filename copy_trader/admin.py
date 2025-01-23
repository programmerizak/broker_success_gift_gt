from django.contrib import admin
from .models import CopyTrader



@admin.register(CopyTrader)
class CopyTraderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'total_trades','loose_percentage','win_percentage', 'no_copiers','date_joined')
    # list_filter = ('status',)
    # search_fields = ('coin_name', 'coin_symbol')
    # date_hierarchy = 'launch_time_start'
    # readonly_fields = ('filled_percent',)