from django.db import models
from services.models import ServiceName
# Create your models here.
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from coupon.models import Coupon

# def validate_file_extension(value):
# 	mime = magic.Magic()
# 	detected_mime = mime.from_buffer(value.read())
	
# 	if "application/x-msdownload" in detected_mime:
# 		raise ValidationError("Detected potential virus or harmful file type.")

# 	# Add more file types and corresponding MIME types to check for potential viruses

# 	# If no issues are detected, reset the file pointer to the beginning
# 	value.seek(0)

###### MORE VALID
# def validate_file_extension(value):
# 	mime = magic.Magic()
# 	detected_mime = mime.from_buffer(value.read())
	
# 	if detected_mime not in ["text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
# 		raise ValidationError("Invalid file type. Only .txt and .docx files are allowed.")

# 	# If no issues are detected, reset the file pointer to the beginning
# 	value.seek(0)



import os

def validate_file_extension(value):
	ext = os.path.splitext(value.name)[1].lower()
	allowed_extensions = ['.txt', '.docx']

	if ext not in allowed_extensions:
		raise ValidationError("Invalid file type. Only .txt and .docx files are allowed.")





class ContactUs(models.Model):
	phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$',
		message = "Valid format: '+9999999999'. Up to 14 digits allowed .")
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone_number = models.CharField(validators=[phone_regex],max_length=15)
	service = models.ForeignKey(ServiceName,on_delete=models.CASCADE,
		related_name="contact_service")
	message = models.TextField()
	#############################################################
	project_file = models.FileField(upload_to='project_files',
	 validators=[validate_file_extension], null=True,blank=True,
	 help_text="Optional: You can attach a project file if needed.\nAccepts only .txt and .docx files")
	#############################################################
	coupon_code = models.CharField(max_length=50, blank=True)
	percent_off = models.PositiveIntegerField(blank=True, null=True)
	#############################################################
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created',]

	def __str__(self):
		return self.name

	@property
	def percentage_off(self):
		if self.coupon_code:
			return f" {self.percent_off} %"
		return " - "


	def save(self, *args, **kwargs):
		if self.pk is None:  # Model instance is being created
			if self.coupon_code:
				try:
					coupon = Coupon.objects.get(code=self.coupon_code, expiration_date__gte=timezone.now())
					self.percent_off = coupon.percentage_reduction
				except Coupon.DoesNotExist:
					pass  # Handle invalid coupon code here if needed

		super().save(*args, **kwargs)