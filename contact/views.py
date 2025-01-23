from django.shortcuts import render, redirect
from .forms import ContactUsForm
from django.contrib import messages
# Create your views here.

def contact(request):
	context = {'page_title':"Contact Us"}
	form = ContactUsForm()
	if request.method == "POST":
		form_data = ContactUsForm(data=request.POST,files=request.FILES)
		if form_data.is_valid():
			form_data.save()
			messages.success(request,"Your message has been received successfully")
		else:
			messages.error(request,"Fill all required information ")
	context['form'] = form
	return render(request,'contact/contact.html',context)


######### HANDLES THE GENERAL FORM SUBMISSION 
def form_submission_view(request):
	if request.method == 'POST':
		form = ContactUsForm(data=request.POST,files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your message has been received successfully!')
		else:
			messages.error(request,"Something not right with the form ")
	# Redirect back to the referring page
	return redirect(request.META.get('HTTP_REFERER', '/'))
