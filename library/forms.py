from django import forms

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)

class DateTimePicker(forms.Form):
	date_time=forms.DateTimeField(label='Checkout Time')
class CheckoutForm(forms.Form):
	check=forms.BooleanField(required=False)