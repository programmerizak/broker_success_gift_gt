from django.contrib import admin
from .models import LaunchPad



@admin.register(LaunchPad)
class LaunchPadAdmin(admin.ModelAdmin):
    list_display = ('coin_name', 'coin_symbol', 'status', 'launch_time_start', 'launch_time_end')
    list_filter = ('status',)
    search_fields = ('coin_name', 'coin_symbol')
    date_hierarchy = 'launch_time_start'
    # readonly_fields = ('filled_percent',)
