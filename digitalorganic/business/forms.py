from django import forms
from django.forms import inlineformset_factory
from .models import ContactQuery,EnquiryItem
from product.models import Product

class ContactForm(forms.Form):
	first_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	message = forms.CharField(widget=forms.Textarea ,required=True)



class OrderForm(forms.ModelForm):
	class Meta:
		model = ContactQuery
		fields = ['first_name','last_name','mobile', 'email','pincode']
		### exclude = ['full_name']
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email

	def clean_full_name(self):
		full_name = self.cleaned_data.get('first_name')
		#write validation code.
		return full_name

