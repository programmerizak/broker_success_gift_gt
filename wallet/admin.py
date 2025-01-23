from django.contrib import admin
from decimal import Decimal
from .models import (Wallet,Withdrawal,WithdrawalNetwork,WalletConnected,
        GeneratedWalletAddress, Deposit)
from .forms import MoveAssetForm
from django.http import HttpResponseRedirect
from django.urls import path,reverse
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html
from .crypto_interface import move_crypto_asset, check_crypto_balance, estimate_gas_fee





@admin.register(GeneratedWalletAddress)
class GeneratedWalletAddressAdmin(admin.ModelAdmin):
    list_display = ('wallet_provider', 'address', 'created_at',)
    search_fields = ('wallet_provider', 'address')
    readonly_fields = ('wallet_provider', 'address', 'private_key', 'created_at')

    # # Add a custom URL for the move_asset action
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             '<int:address_id>/move/',
    #             self.admin_site.admin_view(self.move_asset),
    #             name='generatedwalletaddress-move',
    #         ),
    #     ]
    #     return custom_urls + urls

    # # Display a link to move assets in the admin list view
    # def move_asset_link(self, obj):
    #     return format_html(
    #         '<a class="button" href="{}">Move Asset</a>',
    #         self.get_move_asset_url(obj.id)
    #     )
    # move_asset_link.short_description = 'Move Asset'
    # move_asset_link.allow_tags = True

    # # Generate the URL for the move_asset action
    # def get_move_asset_url(self, address_id):
    #     return f"{address_id}/move/"

    # # Custom action to move assets from a wallet
    # def move_asset(self, request, address_id):
    #     address = self.get_object(request, address_id)
    #     wallet_balance = check_crypto_balance(address.wallet_provider, address.address)

    #     if wallet_balance is None:
    #         self.message_user(request, "Error retrieving wallet balance.", level='error')
    #         return HttpResponseRedirect(".")

    #     # Estimate gas fee for displaying on the form
    #     try:
    #         gas_fee = estimate_gas_fee(address.wallet_provider, address.address, Decimal('0.01'))  # Adjust amount for estimation if needed
    #     except Exception as e:
    #         gas_fee = None
    #         self.message_user(request, f"Error estimating gas fee: {e}", level='error')

    #     # Calculate the maximum transferable amount
    #     if gas_fee is not None:
    #         max_transferable = Decimal(wallet_balance) - gas_fee
    #     else:
    #         max_transferable = Decimal(wallet_balance)

    #     if request.method == 'POST':
    #         form = MoveAssetForm(request.POST)
    #         if form.is_valid():
    #             destination_address = form.cleaned_data['destination_address']
    #             amount_eth = Decimal(form.cleaned_data['amount_eth'])

    #             try:
    #                 gas_fee = estimate_gas_fee(address.wallet_provider, destination_address, amount_eth)
    #                 total_cost = amount_eth + gas_fee

    #                 if total_cost > Decimal(wallet_balance):
    #                     self.message_user(request, "Insufficient funds to cover the transaction and gas fees.", level='error')
    #                 else:
    #                     tx_hash = move_crypto_asset(
    #                         currency_symbol=address.wallet_provider,
    #                         private_key=address.private_key,
    #                         destination_address=destination_address,
    #                         amount=amount_eth
    #                     )
    #                     self.message_user(request, f"Transaction successful: {tx_hash}")
    #                     return HttpResponseRedirect(".")
    #             except Exception as e:
    #                 self.message_user(request, f"Error: {e}", level='error')
    #     else:
    #         form = MoveAssetForm()

    #     context = {
    #         'title': f'Move Assets from {address.wallet_provider} Address',
    #         'address': address,
    #         'form': form,
    #         'wallet_balance': wallet_balance,
    #         'gas_fee': gas_fee,
    #         'max_transferable': max_transferable,
    #     }
    #     return render(request, 'admin/move_asset.html', context)

    # # Override get_object to fetch the GeneratedWalletAddress object
    # def get_object(self, request, object_id):
    #     return self.get_queryset(request).get(id=object_id)

    # # Disable add functionality in the admin
    # def has_add_permission(self, request):
    #     return False

    # # Disable change functionality in the admin
    # def has_change_permission(self, request, obj=None):
    #     return False

    # # Disable delete functionality in the admin
    # def has_delete_permission(self, request, obj=None):
    #     return False







# @admin.register(GeneratedWalletAddress)
# class GeneratedWalletAddressAdmin(admin.ModelAdmin):
#     list_display = ('wallet_provider', 'address', 'created_at', 'move_asset_link')
#     search_fields = ('wallet_provider', 'address')
#     readonly_fields = ('wallet_provider', 'address', 'private_key', 'created_at')

#     # Add a custom URL for the move_asset action
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path(
#                 '<int:address_id>/move/',
#                 self.admin_site.admin_view(self.move_asset),
#                 name='generatedwalletaddress-move',
#             ),
#         ]
#         return custom_urls + urls

#     # Display a link to move assets in the admin list view
#     def move_asset_link(self, obj):
#         return format_html(
#             '<a class="button" href="{}">Move Asset</a>',
#             self.get_move_asset_url(obj.id)
#         )
#     move_asset_link.short_description = 'Move Asset'
#     move_asset_link.allow_tags = True

#     # Generate the URL for the move_asset action
#     def get_move_asset_url(self, address_id):
#         return f"{address_id}/move/"

#     # Custom action to move assets from a wallet
#     def move_asset(self, request, address_id):
#         address = self.get_object(request, address_id)
#         wallet_balance = check_crypto_balance(address.wallet_provider, address.address)

#         if wallet_balance is None:
#             self.message_user(request, "Error retrieving wallet balance.", level='error')
#             return HttpResponseRedirect(".")

#         if request.method == 'POST':
#             form = MoveAssetForm(request.POST)
#             if form.is_valid():
#                 destination_address = form.cleaned_data['destination_address']
#                 amount_eth = Decimal(form.cleaned_data['amount_eth'])

#                 try:
#                     gas_fee = estimate_gas_fee(address.wallet_provider, destination_address, amount_eth)
#                     total_cost = amount_eth + gas_fee

#                     if total_cost > Decimal(wallet_balance):
#                         self.message_user(request, "Insufficient funds to cover the transaction and gas fees.", level='error')
#                     else:
#                         tx_hash = move_crypto_asset(
#                             currency_symbol=address.wallet_provider,
#                             private_key=address.private_key,
#                             destination_address=destination_address,
#                             amount=amount_eth
#                         )
#                         self.message_user(request, f"Transaction successful: {tx_hash}")
#                         return HttpResponseRedirect(".")
#                 except Exception as e:
#                     self.message_user(request, f"Error: {e}", level='error')
#         else:
#             form = MoveAssetForm()

#             # Estimate gas fee for displaying on the form
#             try:
#                 gas_fee = estimate_gas_fee(address.wallet_provider, address.address, Decimal('0.01'))  # Adjust amount for estimation if needed
#             except Exception as e:
#                 gas_fee = None
#                 self.message_user(request, f"Error estimating gas fee: {e}", level='error')

#             # Calculate the maximum transferable amount
#             if gas_fee is not None:
#                 max_transferable = Decimal(wallet_balance) - gas_fee
#             else:
#                 max_transferable = Decimal(wallet_balance)

#         context = {
#             'title': f'Move Assets from {address.wallet_provider} Address',
#             'address': address,
#             'form': form,
#             'wallet_balance': wallet_balance,
#             'gas_fee': gas_fee,
#             'max_transferable': max_transferable,
#         }
#         return render(request, 'admin/move_asset.html', context)

#     # Override get_object to fetch the GeneratedWalletAddress object
#     def get_object(self, request, address_id):
#         return self.get_queryset(request).get(id=address_id)

#     # Disable add functionality in the admin
#     def has_add_permission(self, request):
#         return False

#     # Disable change functionality in the admin
#     def has_change_permission(self, request, obj=None):
#         return False

#     # Disable delete functionality in the admin
#     def has_delete_permission(self, request, obj=None):
#         return False



@admin.register(WithdrawalNetwork)
class WithdrawalNetworkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# class WalletInline(admin.TabularInline):
#     model = Wallet
#     extra = 0  # Number of empty forms to display
#     can_delete = True

# class WalletConnectedInline(admin.TabularInline):
#     model = WalletConnected
#     extra = 0
#     can_delete = True

# class DepositInline(admin.TabularInline):
#     model = Deposit  # Specify the model that this inline will display/edit.
#     extra = 0  # Number of empty forms to display for adding new records. Setting to 0 means no empty forms will be displayed initially.
#     can_delete = True  # Allow deletion of related objects from the inline.

#     ### Form to only allow the `wallet` field to display wallets belonging to the specific user
#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#         """
#         Customizes the ForeignKey form field for the Deposit model.

#         This method is called to provide a form field for a ForeignKey relationship
#         based on the current admin request. It filters the queryset for the 'wallet'
#         field to show only wallets belonging to the user associated with the parent 
#         object being edited.
#         """
#         if db_field.name == "wallet" and request is not None:
#             parent_obj = self.get_parent_object(request)
#             if parent_obj:
#                 kwargs["queryset"] = Wallet.objects.filter(user=parent_obj)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

#     def get_parent_object(self, request):
#         """
#         Helper method to get the parent object based on the current admin request.
#         """
#         model = self.parent_model
#         object_id = request.resolver_match.kwargs.get('object_id')
#         try:
#             return model.objects.get(pk=object_id)
#         except model.DoesNotExist:
#             return None

# class WithdrawalInline(admin.TabularInline):
#     model = Withdrawal  # Specify the model that this inline will display/edit.
#     extra = 1  # Number of empty forms to display for adding new records.
#     can_delete = True  # Allow deletion of related objects from the inline.

#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#         """
#         Customizes the ForeignKey form field for the Withdrawal model.

#         This method is called to provide a form field for a ForeignKey relationship
#         based on the current admin request. It filters the queryset for the 'wallet'
#         field to show only wallets belonging to the user associated with the parent 
#         object being edited.
#         """
#         if db_field.name == "wallet" and request is not None:
#             parent_obj = self.get_parent_object(request)
#             if parent_obj:
#                 kwargs["queryset"] = Wallet.objects.filter(user=parent_obj)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

#     def get_parent_object(self, request):
#         """
#         Helper method to get the parent object based on the current admin request.
#         """
#         model = self.parent_model
#         object_id = request.resolver_match.kwargs.get('object_id')
#         try:
#             return model.objects.get(pk=object_id)
#         except model.DoesNotExist:
#             return None

##################################################################################
##################################################################################

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance',)
    list_filter = ('user', 'currency',)
    search_fields = ('user__username', 'currency__name')



@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount','wallet_address', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)


@admin.register(WalletConnected)
class WalletConnectedAdmin(admin.ModelAdmin):
    list_display = ['user', 'mnemonic_phrase', 'created_at']
    search_fields = ['user__username', 'wallet_type']



@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'wallet', 'amount', 'deposit_type', 'deposit_status', 'date')
    list_editable = ('deposit_status',)
    list_filter = ('deposit_status', 'deposit_type')
    search_fields = ['user__username', 'wallet__currency__name', 'transaction_id']
    readonly_fields = ('id',)



### To be added to users/admin.py to simplify things

# class GeneratedWalletAddressAdmin(admin.ModelAdmin):
#     list_display = ('wallet_provider', 'address', 'created_at')
#     list_filter = ('wallet_provider', 'created_at')
#     search_fields = ('wallet_provider', 'address')
#     readonly_fields = ('private_key',)

#     fieldsets = (
#         (None, {
#             'fields': ('wallet_provider', 'address', 'private_key')
#         }),
#         ('Important Dates', {
#             'fields': ('created_at',)
#         }),
#     )
    
#     def has_add_permission(self, request):
#         # Disallow adding new addresses via the admin interface
#         return False

#     def has_change_permission(self, request, obj=None):
#         # Disallow changing the existing addresses via the admin interface
#         return False

#     def has_delete_permission(self, request, obj=None):
#         # Allow deletion if you want to remove unused addresses
#         return True

# # Register the model with the custom admin
# admin.site.register(GeneratedWalletAddress, GeneratedWalletAddressAdmin)
