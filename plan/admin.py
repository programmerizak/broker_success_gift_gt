from django.contrib import admin
from .models import Plan, UserPlan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'minimum', 'maximum', 'duration', 'roi')  # Fields to display in the list view
    search_fields = ('plan_name',)  # Fields to enable search functionality
    list_filter = ('duration',)  # Fields to filter by in the admin panel
    ordering = ('plan_name',)  # Default ordering of plans
    fields = ('plan_name', 'minimum', 'maximum', 'duration', 'roi')  # Fields to display in the edit form


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount_invested', 'start_date', 'end_date', 'status')  # Fields to display
    search_fields = ('user__username', 'plan__plan_name')  # Enable search by related fields
    list_filter = ('status', 'plan__plan_name', 'start_date', 'end_date')  # Fields to filter by
    ordering = ('-start_date',)  # Default ordering (most recent first)
    fields = ('user', 'plan', 'amount_invested', 'start_date', 'end_date', 'status')  # Fields to display in the edit form
    readonly_fields = ('start_date', 'end_date')  # Make start_date and end_date read-only in the admin form


