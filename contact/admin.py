from django.contrib import admin
from .models import ContactUs

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
	list_display = ['name','email','phone_number','percentage_off','created']
	search_fields = ['name','percentage_off',]
