from django.contrib import admin
from .models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'is_crypto')
    list_filter = ('is_crypto',)
    search_fields = ('name', 'symbol')
    ordering = ('name',)