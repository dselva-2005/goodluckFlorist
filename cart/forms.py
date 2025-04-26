from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(initial=1,widget=forms.NumberInput(attrs={'min': 1, 'max': 100}))
    override = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)


class MessageForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5
        })
    )
