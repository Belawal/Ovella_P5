from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                 'street_address1', 'street_address2',
                 'town_or_city', 'postcode', 'country',
                 'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        Also handles django-countries field choices conversion.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'county': 'County',
            'country': 'Country',
        }

        # Special handling for django-countries field
        if 'country' in self.fields:
            try:
                # Convert choices to list and assign to both field and widget
                country_choices = list(self.fields['country'].choices)
                self.fields['country'].choices = country_choices
                self.fields['country'].widget.choices = country_choices
            except (TypeError, AttributeError):
                # Fallback in case the choices can't be converted
                pass

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field_name, field in self.fields.items():
            if field.required:
                placeholder = f'{placeholders.get(field_name, "")} *'
            else:
                placeholder = placeholders.get(field_name, "")
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'stripe-style-input'
            field.label = False