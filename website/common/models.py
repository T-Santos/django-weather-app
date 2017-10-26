from django.db import models

class SignupLocation(models.Model):

	city = models.CharField(max_length = 50)
	state = models.ForeignKey('state')

	def __str__(self):
		return '{}, {}'.format(self.city,self.state.code)

	class Meta:
		ordering = ['city']

class State(models.Model):

	code = models.CharField(max_length = 2)
	name = models.CharField(max_length = 50)

	def __str__(self):

		return '{}, {}'.format(self.name,self.code)



