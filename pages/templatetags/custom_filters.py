from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to a form field
    
    Usage in template: {{ form.field|add_class:'my-class' }}
    """
    if isinstance(value, BoundField):
        # Get the current class attribute or create an empty string
        current_class = value.field.widget.attrs.get('class', '')
        
        # Combine existing classes with new class
        new_classes = f"{current_class} {arg}".strip()
        
        # Set the new class attribute
        value.field.widget.attrs['class'] = new_classes
    
    return value