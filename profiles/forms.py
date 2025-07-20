from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_postcode': 'Postal Code',
            'default_county': 'County',
            'default_country': 'Country',
        }

        # Special handling for django-countries field
        if 'default_country' in self.fields:
            try:
                country_choices = list(self.fields['default_country'].choices)
                self.fields['default_country'].choices = country_choices
                self.fields['default_country'].widget.choices = country_choices
            except (TypeError, AttributeError):
                pass

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field_name, field in self.fields.items():
            placeholder = placeholders.get(field_name, "")
            if field.required:
                placeholder += " *"
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            field.label = False
