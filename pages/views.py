from django.shortcuts import render,redirect,get_object_or_404
from wallet.tasks import my_task
from django.core.mail import send_mail
from django.conf import settings
from wallet.tasks import run_check_trades


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
import sweetify

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
	run_check_trades.delay()
	return render(request, 'pages/home_page.html',context)


def about_page(request):
	page_title = "About Us"
	context = {'page_title':page_title}
	return render(request, 'pages/about_page.html',context)


# def contact_page(request):
# 	page_title = "Contact Us"
# 	context = {'page_title':page_title}
# 	return render(request, 'pages/contact_page.html',context)


def contact_page(request):
    """
    View to handle contact form submission using ModelForm
    """
    if request.method == 'POST':
        # Create form instance with POST data
        form = ContactForm(request.POST)
        
        # Validate the form
        if form.is_valid():
            # Save the form (creates a model instance)
            contact_message = form.save()

            # Optional: Send email notification
            # try:
            #     send_mail(
            #         f'New Contact Message: {contact_message.subject}',
            #         f'From: {contact_message.name}\n'
            #         f'Email: {contact_message.email}\n'
            #         f'Phone: {contact_message.phone or "N/A"}\n\n'
            #         f'Message:\n{contact_message.message}',
            #         settings.DEFAULT_FROM_EMAIL,
            #         [settings.CONTACT_EMAIL],
            #         fail_silently=False,
            #     )
            # except Exception as e:
            #     # Log the error, but don't prevent form submission
            #     print(f"Email sending failed: {e}")

            # Add success message
            # messages.success(request, 'Your message has been sent successfully!')
            sweetify.success(request,'Your message has been sent successfully!')
            return redirect('pages:contact_page')
    else:
        # Create a blank form for GET request
        form = ContactForm()

    # Render the template with the form
    return render(request, 'pages/contact_page.html', {'form': form})



def terms_page(request):
	page_title = "Terms and Conditions"
	context = {'page_title':page_title}
	return render(request, 'pages/terms_page.html',context)



def privacy_page(request):
	page_title = "Privacy Policy"
	context = {'page_title':page_title}
	return render(request, 'pages/privacy_page.html',context)