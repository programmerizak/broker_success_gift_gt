from django.contrib import admin
from .models import StakePlan, Stake, Duration


@admin.register(StakePlan)
class StakePlanAdmin(admin.ModelAdmin):
    list_display = ['coin', 'minimum_stake_amount', 'maximum_stake_amount', 'active', 'created_at']
    list_filter = ('active', 'created_at')
    search_fields = ('coin__name', 'coin__symbol')
    ordering = ('-created_at',)
    # readonly_fields = ['created_at']
    filter_horizontal = ['durations']


@admin.register(Stake)
class StakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'stake_plan', 'stake_amount','estimated_return','stake_outcome','stake_status', 'start_date', 'end_date']
    list_filter = ['stake_status']
    search_fields = ['user__username', 'stake_plan__coin__name']
    readonly_fields = ['end_date','stake_outcome','estimated_return',]
    # readonly_fields = ['start_date', 'end_date']



@admin.register(Duration)
class DurationAdmin(admin.ModelAdmin):
    list_display = ['duration_days', 'percentage_return']


