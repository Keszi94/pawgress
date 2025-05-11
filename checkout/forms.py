from django import forms
from .models import Purchase


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'email': 'Email address',
        }

        # sets the autofocus on the email field
        self.fields['email'].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            # adds a star to required fields
            placeholder = placeholders.get(field_name, '')
            if field.required:
                placeholder += ' *'
            field.widget.attrs['placeholder'] = placeholder

            # custom css class
            field.widget.attrs['class'] = 'stripe-style-input'
            # hides the label - placeholder enough
            field.label = False
