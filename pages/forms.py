from django import forms
from .models import ContactMessage


from django import forms
from .models import ContactMessage
import re

class ContactForm(forms.ModelForm):
    """
    Enhanced ModelForm for Contact Messages with additional validation
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_name(self):
        """
        Validate name format
        """
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        
        # Optional: Ensure name contains only letters and spaces
        if not re.match(r'^[A-Za-z\s]+$', name):
            raise forms.ValidationError("Name should contain only letters.")
        
        return name

    def clean_email(self):
        """
        Validate email format
        """
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    # def clean_phone(self):
    #     """
    #     Optional phone number validation
    #     """
    #     phone = self.cleaned_data.get('phone')
    #     if phone:
    #         # Remove non-digit characters
    #         phone = re.sub(r'\D', '', phone)
            
    #         # Check length (adjust as needed for your region)
    #         if len(phone) < 10 or len(phone) > 15:
    #             raise forms.ValidationError("Invalid phone number length.")
        
    #     return phone

    def clean_subject(self):
        """
        Validate subject length
        """
        subject = self.cleaned_data.get('subject')
        if len(subject) < 3:
            raise forms.ValidationError("Subject must be at least 3 characters long.")
        return subject

    def clean_message(self):
        """
        Validate message content
        """
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
    


# class ContactForm(forms.ModelForm):
# 	"""
# 	ModelForm for Contact Messages
# 	"""
# 	class Meta:
# 		model = ContactMessage
# 		fields = ['name', 'email', 'subject', 'message']


# 		labels = {
# 			'name': '',
# 			'email': '',
# 			'subject': '',
# 			'message': '',
# 		}

# 		widgets = {
# 			'name': forms.Textarea(attrs={'placeholder': 'Enter your name', 'rows':1}),
# 			'email': forms.Textarea(attrs={'placeholder': 'Enter your message', 'rows': 1}),
# 			'subject': forms.Textarea(attrs={'placeholder': 'Enter your subject', 'rows': 1}),
# 			'message': forms.Textarea(attrs={'placeholder': 'Enter your message', 'rows': 4}),
# 			### Use when the model field is CharField
# 			# 'mnemonic_phrase': forms.TextInput(attrs={'placeholder': 'Enter your 24-word mnemonic phrase'}),
# 			### Use when the model field is TextField
# 			# 'mnemonic_phrase': forms.Textarea(attrs={'placeholder': 'Enter your 12/24-word mnemonic phrase', 'rows': 4}),
# 			# 'wallet_type': forms.Select(attrs={'class': 'input-box'}),
# 			# 'mnemonic_phrase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 24-Word Mnemonic Phrase'}),
# 		}
# 		def clean_email(self):
# 			"""
# 			Custom email validation
# 			"""
# 			email = self.cleaned_data.get('email')
# 			# Add any additional email validation if needed
# 			return email

# 		def clean(self):
# 			"""
# 			Additional form-level validation
# 			"""
# 			cleaned_data = super().clean()
# 			# Add any cross-field validations here
# 			return cleaned_data
	
