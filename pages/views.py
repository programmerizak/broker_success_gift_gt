from django.shortcuts import render,redirect,get_object_or_404
from wallet.tasks import my_task
from django.core.mail import send_mail
from django.conf import settings
# from wallet.tasks import run_check_trades

# # Send an email
# def send_test_email():
#     subject = "Test Email from Django"
#     message = "This is a test email sent from Django!"
#     from_email = settings.DEFAULT_FROM_EMAIL  # Default email in settings
#     recipient_list = ['themporst1@gmail.com']  # List of recipient emails

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Error sending email: {e}")

def home_page(request):
	context = {}
	page_title = "Home"
	context['page_title'] = page_title
	# send_test_email()
	# Trigger the Celery task
	# run_check_trades.delay()
	return render(request, 'pages/home_page.html',context)


def about_page(request):
	page_title = "About Us"
	context = {'page_title':page_title}
	return render(request, 'pages/about_page.html',context)


def contact_page(request):
	page_title = "Contact Us"
	context = {'page_title':page_title}
	return render(request, 'pages/contact_page.html',context)



def terms_page(request):
	page_title = "Terms and Conditions"
	context = {'page_title':page_title}
	return render(request, 'pages/terms_page.html',context)



def privacy_page(request):
	page_title = "Privacy Policy"
	context = {'page_title':page_title}
	return render(request, 'pages/privacy_page.html',context)