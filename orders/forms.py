from django import forms
from .models import Order
from django.utils import timezone
from datetime import timedelta
import pytz

class OrderCreateForm(forms.ModelForm):

    payment_mode = forms.ChoiceField(choices= [
        ('COD', 'Cash on delivery'),
        ('ONLINE_PAYMENT', 'Online payment'),
    ])

    desired_delivery_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'min': (timezone.now().astimezone(pytz.timezone('Asia/Kolkata')) + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M'),
                'class': 'form-control',  # Bootstrap form-control class
                'style': 'background-color: #f5f7fa;',  # Light grey background
            }
        ),
        label="Desired Delivery Date and Time",
         help_text="The delivery time may vary depending on the location. If we can't reach the arrangement at the specified time, we will get in touch with you."
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
        'postal_code', 'city']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'First Name',
                'required': 'required',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'last_name',
                'placeholder': 'Last Name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Email',
                'required': 'required',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'id': 'street_address',
                'placeholder': 'Address',
                'required': 'required',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'zipCode',
                'placeholder': 'Zip Code',
                'required': 'required',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
                'placeholder': 'Town',
                'required': 'required',
            }),
        }