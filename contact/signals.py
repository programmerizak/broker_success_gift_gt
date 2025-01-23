from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import decimal,random,string,django
from django.shortcuts import get_object_or_404
from django.conf import settings
from decimal import Decimal
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import render_to_string, get_template

from .models import ContactUs



@receiver(post_save, sender=ContactUs)
def do_after_save(sender, instance, created, **kwargs):
	if created:
		#Send Email

		# Send email to yourself
		subject = 'New Contact Form Submission'
		template = get_template('contact/notify_admin_email.html')
		context = {'name': instance.name, 'email': instance.email}
		html_message = template.render(context)
		from_email = settings.DEFAULT_FROM_EMAIL
		recipient_list = [settings.YOUR_EMAIL_ADDRESS]  # Replace with your email address
		email = EmailMessage(subject, html_message, from_email, recipient_list)
		email.content_subtype = 'html'
		email.send()



		# Send email to the person who filled the form
		user_subject = 'Thank you for contacting us'
		user_template = get_template('contact/notify_user_email.html')
		user_html_message = user_template.render({})
		user_from_email = settings.DEFAULT_FROM_EMAIL
		user_recipient_list = [instance.email]
		user_email = EmailMessage(user_subject, user_html_message, user_from_email, user_recipient_list)
		user_email.content_subtype = 'html'
		user_email.send()



	# name = models.CharField(max_length=100)
	# email = models.EmailField()
	# phone_number = models.CharField(validators=[phone_regex],max_length=15)
	# service = models.ForeignKey(ServiceName,on_delete=models.CASCADE,
	# 	related_name="contact_service")
	# message = models.TextField()
	# #############################################################
	# project_file = models.FileField(upload_to='project_files',
	#  validators=[validate_file_extension], null=True,blank=True,
	#  help_text="Optional: You can attach a project file if needed.\nAccepts only .txt and .docx files")
	# #############################################################24+
	# coupon_code = models.CharField(max_length=50, blank=True)
	# percent_off = models.P3274//56/ -98+6