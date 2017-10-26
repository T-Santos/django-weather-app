from django.db import models

from common.models import SignupLocation

class WeatherSignup(models.Model):

	email_address = models.EmailField(
						"email address",
						unique = True,
						)
	location = models.ForeignKey('common.SignupLocation')

	class Meta:
		verbose_name = 'Subscriber'
		verbose_name_plural = 'Subscribers'

	def __str__(self):

		return self.email_address

	# to be used to allow for unsubscribe/subscribe funct
	weather_email_active = models.BooleanField(default = True)

	def __str__(self):

		return str(self.email_address)


