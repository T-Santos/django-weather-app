"""
The purpose of this module is to contain functionality supporting the e-mailing 
of users signed up to receive weather based emails. Supporting documentation about calling
is included in the django management command.
"""

# 3rd party supporting packages
import unidecode
import arrow

# django built-in packages
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

# local django project
from weather.models import WeatherSignup
from weather.utilities.extract.weather import ExtractWeather

def is_warmer_than_avg(cur_temp,avg_temp,threshold):
	"""
	Purpose: Determine if the current temp is warmer than the average temp
				while being outside the avg_temp/threshold window
	cur_temp: int
	avg_temp: int
	threshold: pos int
	"""

	if threshold < 0:
		raise ValueError("threshold must be a positive int")

	if cur_temp >= avg_temp:

		if avg_temp + threshold <= cur_temp:
			return True

	return False

def is_cooler_than_avg(cur_temp,avg_temp,threshold):
	"""
	Purpose: Determine if the current temp is cooler than the average temp
				while being outside the avg_temp/threshold window
	cur_temp: int
	avg_temp: int
	threshold: pos int
	"""

	if threshold < 0:
		raise ValueError("threshold must be a positive int")

	if cur_temp <= avg_temp:

		if avg_temp - threshold >= cur_temp:
			return True

	return False

def email_subscribers(api_key):	
	"""
	Purpose: For users that have active subscriptions to the weather application, 
				send them personalized emails based on the current weather in their
				specified locations in respect to the average temperature for that location.
	Considerations: Should we be getting the time based on server's location? How does that impact
					getting the current temp? For mornings on west coast compared to an avg daily temp
					is likely going to be lower on average because of the time we are getting the current temp.
					Might want to get it at noon or several times throughout the day.
	"""

	# global settings
	FROM_EMAIL = settings.EMAIL_HOST_USER
	WEATHER_CREDIT_IMG_URL = 'https://www.wunderground.com/logos/images/wundergroundLogo_4c_horz.jpg'
	WEATHER_CREDIT_URL = 'https://www.wunderground.com'

	NICE_SUBJECT = "It's nice out! Enjoy a discount on us."
	BAD_SUBJECT = "Not so nice out? That's okay, enjoy a discount on us."
	DEF_SUBJECT = "Enjoy a discount on us."

	THRESHOLD = 5
	PRECIP_KEYWORD_LIST = ['rain','mist','snow','hail','drizzle','ice','precipitation']

	weather = ExtractWeather(api_key)	# Used to interface with 3rd party weather API
	subscribers = WeatherSignup.objects.filter(weather_email_active=True)	# used to get all activesubscribers

	location_weather_dict = {}	# cache already computed location -> weather data
	email_data = []		# final list of computed data ready to be emailed

	for subscriber in subscribers:
		state = subscriber.location.state.code
		city = subscriber.location.city
		ascii_city = unidecode.unidecode(city)

		# get cached value for location else calculate it
		if (ascii_city,state) in location_weather_dict:
			[todays,today_historical] = location_weather_dict[ascii_city,state]
		else:
			[todays,today_historical] = weather.for_features(state,ascii_city,today=True,today_historical=True)
			location_weather_dict[ascii_city,state] = [todays,today_historical]

		if todays and today_historical:

			# get rough representations of temps
			high_temp = round(float(today_historical.high_avg_temp_f))
			low_temp = round(float(today_historical.low_avg_temp_f))
			now_temp = round(float(todays.temp_f))

			# not the most accurate since its the avg of rounded avgs but its close enough
			avg_temp = round((high_temp + low_temp)/2)

			# compute subject
			if todays.weather.lower() == 'clear':
				subject = NICE_SUBJECT
			elif set([word.lower() for word in todays.weather.split(" ")]).intersection(PRECIP_KEYWORD_LIST):
				subject = BAD_SUBJECT
			elif is_warmer_than_avg(now_temp,avg_temp,THRESHOLD):
				subject = NICE_SUBJECT
			elif is_cooler_than_avg(now_temp,avg_temp,THRESHOLD):
				subject = BAD_SUBJECT
			else:
				subject = DEF_SUBJECT

			# compute message
			message = 'In {} the temperature is {} and {}.'.format(
						str(subscriber.location),
						todays.temp_pretty,
						todays.weather)

			# compute html message
			html_message = loader.render_to_string(
							'weather/email.html',
							{
								'weather_link': todays.extract_value(['icon_url']),
								'weather_credit': WEATHER_CREDIT_IMG_URL,
								'weather_credit_url': WEATHER_CREDIT_URL,
								'weather_msg': message,
							})
			recipient_list = [subscriber.email_address]

			# add it to the list ( this is helpful for bulk emails...which we can't do yet)
			# we could just send them out one by one here instead of iterating again at the end
			email_data.append(((subject,message,FROM_EMAIL,recipient_list),{"html_message":html_message}))	

	# sending bulk email currently doesnt allow
	# for html messages. Could hack it if necessary
	# to allow bulk wrapper to accept html_message
	# or param to just send utf-8 and forget the html
	for (email_args,email_kwargs) in email_data:
		send_mail(*email_args,**email_kwargs)

	return (len(email_data),len(subscribers))