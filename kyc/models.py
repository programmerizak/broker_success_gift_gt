from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from easy_thumbnails.fields import ThumbnailerImageField


class Kyc(models.Model):
	phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$',
		message = "Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed .")
	verify_choices = (
		('unverified','unverified'),
		('verified','verified'),
		)
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_kyc')
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email_address = models.EmailField()
	date_of_birth = models.DateField()
	phone_number = models.CharField(validators=[phone_regex],max_length=15,blank=True)
	# telegram_username = models.CharField(max_length=30, blank=True)
	address_line_1 = models.CharField(max_length=200)
	address_line_2 = models.CharField(max_length=200,blank=True,help_text="Optional")
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	nationality = models.CharField(max_length=200)
	zip_code = models.CharField(max_length=20)
	ID_front =ThumbnailerImageField(upload_to='kyc/id_front')
	ID_back =ThumbnailerImageField(upload_to='kyc/id_back')
	verify_status = models.CharField(choices = verify_choices,default='unverified',max_length=50)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return self.user.username
