from django.contrib import admin
from .models import Kyc
from django.utils.html import format_html

@admin.register(Kyc)
class KycAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'email_address', 'phone_number', 
        'verify_status', 'created', 'updated', 'view_id_front', 'view_id_back'
    )
    list_filter = ('verify_status', 'created', 'updated')
    search_fields = ('user__username', 'email_address', 'phone_number', 'first_name', 'last_name')
    date_hierarchy = 'created'
    ordering = ('-created',)

    def view_id_front(self, obj):
        if obj.ID_front:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.ID_front.url)
        return "No image"
    view_id_front.short_description = "ID Front"

    def view_id_back(self, obj):
        if obj.ID_back:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.ID_back.url)
        return "No image"
    view_id_back.short_description = "ID Back"
