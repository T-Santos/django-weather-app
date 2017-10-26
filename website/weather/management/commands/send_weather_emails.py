"""
This source is to contain functionality supporting the django management command for 
sending emails weather subscribers

o When WEATHER_API_KEY os.env variable is set
ex: python3 manage.py send_weather_emails

o When API_KEY commandline arg is passed
ex: python3 manage.py --API_KEY XXXXXXXXXXX

"""
from django.core.management.base import BaseCommand, CommandError

from weather.utilities.email import email_subscribers
from weather.conf import settings

class Command(BaseCommand):

	help = 'Send weather based emails based on active subscriptions.'

	def add_arguments(self, parser):

		# optional arg
		parser.add_argument(
			'--API_KEY',
			dest='WEATHER_API_KEY',
			help='Weather API Key',
			)

	def handle(self, *args, **options):

		if 'WEATHER_API_KEY' in options:
			weather_api_key = options['WEATHER_API_KEY']
		else:
			weather_api_key = settings.WEATHER_API_KEY

		if weather_api_key:
			(sent_count,total_count) = email_subscribers(api_key=weather_api_key)
			out_string = "Successfully sent {} of {} active weather e-mail subscriptions.".format(
							sent_count,
							total_count,
							)
			self.stdout.write(self.style.SUCCESS(out_string))
		else:
			self.stdout.write(self.style.WARNING('Weather api key not set. Weather based e-mail not sent.'))