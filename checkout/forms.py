from django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from .models import Purchase


class PurchaseForm(forms.ModelForm):

    country = forms.ChoiceField(
        choices=[('', 'Country *')] + list(CountryField().choices),
        widget=CountrySelectWidget(),
        required=True
    )

    class Meta:
        model = Purchase
        fields = ('email', 'full_name', 'company_name',
                  'street_address1', 'street_address2',
                  'city', 'postcode', 'country')

        labels = {
            'email': 'Email address',
            'full_name': 'Full Name*',
            'company_name': 'Company Name (Optional)',
            'street_address1': 'Street Address 1*',
            'street_address2': 'Street Address 2',
            'city': 'City*',
            'postcode': 'ZIP/Postal code',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # sets the autofocus on the email field
        self.fields['email'].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'stripe-style-input'
