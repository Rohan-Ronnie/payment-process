from django import forms
from payment.models.payment_model import payment_details


class payment_detailsForm(forms.ModelForm):
    class Meta:
        model = payment_details
        exclude = ()