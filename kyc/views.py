
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Kyc
from .forms import KycForm
import sweetify

# Ensure that the user is logged in before they can access the form
@login_required
def kyc_form(request):
	user = request.user
	try:
		# If the user already has a KYC record, we update it
		kyc_instance = Kyc.objects.get(user=request.user)
	except Kyc.DoesNotExist:
		kyc_instance = None

	if request.method == 'POST':
		form = KycForm(request.POST, request.FILES, instance=kyc_instance)
		if form.is_valid():
			data_form = form.save(commit=False)
			data_form.user = user
			data_form.save()
			# Show a success message using SweetAlert
			# messages.success(request, 'Your KYC information has been successfully updated!')
			
			sweetify.success(
				request,
				"Update Successfully",
				text=f"Your KYC information has been successfully updated!",
				persistent="Close",
			)

			return redirect("kyc:kyc_form")


		else:
			# Show an error message using SweetAlert
			# messages.error(request, 'There was an error updating your KYC information. Please try again.')
		
			sweetify.error(
				request,
				"Update Unsuccessfully",
				text=f"There was an error updating your KYC information. Please try again.",
				persistent="Close",
			)

			return redirect("kyc:kyc")


	else:
		form = KycForm(instance=kyc_instance)

	return render(request, 'kyc/kyc_form.html', {'form': form})
