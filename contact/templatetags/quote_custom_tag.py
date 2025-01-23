from django import template
from contact.forms import ContactUsForm

register = template.Library()

@register.inclusion_tag('contact/quote_form.html')
def render_model_form():
	quote_form = ContactUsForm()
	return {'quote_form': quote_form}
