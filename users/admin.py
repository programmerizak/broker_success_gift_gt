from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from wallet.admin import WalletInline, WithdrawalInline, WalletConnectedInline, DepositInline


class UserAdmin(UserAdmin):
	add_form = UserCreationForm
	form = UserChangeForm
	model = User
	list_display = ['username', 'email','trade_outcome','stake_outcome','country', 'profile_verified','date_joined']
	list_editable = ['profile_verified','trade_outcome','stake_outcome',]
	ordering = ['-date_joined',]  # Specify the desired ordering
	fieldsets = UserAdmin.fieldsets + (
			# ('Personal Information', {'fields': ('first_name','last_name')}),  
			('Profile Detail', {'fields': ('profile_picture',
				'gender','country',)}),
			('Profile Verification ', {'fields': ('profile_verified',)}),
	)
	# inlines = [WalletInline, WithdrawalInline, WalletConnectedInline, DepositInline]
admin.site.register(User, UserAdmin)