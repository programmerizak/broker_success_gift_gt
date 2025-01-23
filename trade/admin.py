from django.contrib import admin
from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'trade_pair', 'trading_amount','expected_payout','trade_outcome','trade_status','wallet','start_time','end_time' ,'duration',)
    list_filter = ('user', 'trade_status', 'trade_type')
    search_fields = ('user__username', 'trade_pair')
    date_hierarchy = 'start_time'
    readonly_fields = ('trade_id', 'expected_payout', 'created', 'updated')

    fieldsets = (
        (None, {
            'fields': ('user', 'trade_pair', 'wallet', 'trading_amount', 'start_time', 'duration')
        }),
        ('Trade Details', {
            'fields': ('trade_id', 'expected_payout', 'strike_rate', 'trade_status', 'trade_type')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # Editing an existing object
            return readonly_fields + ('user', 'trade_pair', 'wallet', 'start_time')
        return readonly_fields

    # def has_add_permission(self, request):
    #     return False  # Disable manual addition of Trade objects from admin panel
