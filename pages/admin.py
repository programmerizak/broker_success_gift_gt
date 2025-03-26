from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for Contact Messages
    """
    list_display = ('name', 'email', 'subject', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        """
        Custom admin action to mark selected messages as processed
        """
        queryset.update(is_processed=True)
    mark_as_processed.short_description = "Mark selected messages as processed"