from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import WeatherSignup

class SubscribeWeather(forms.ModelForm):

	def __init__(self,*args,**kwargs):
		super(SubscribeWeather,self).__init__(*args,**kwargs)

		self.fields['location'].empty_label = 'Where do you live?'
		self.fields['email_address'].label = "Email Address"

		self.helper = FormHelper()
		self.helper.form_id = 'id-SubscribeWeather'
		self.helper.add_input(Submit('submit', 'Subscribe', css_class='btn-primary'))

	class Meta:

		model = WeatherSignup
		fields = ['email_address','location']