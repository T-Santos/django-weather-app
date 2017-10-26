"""
This module contains class definitions to interface with a 3rd party weather supplier. This
is to be used as an abstraction layer such that if the supplier changes, references hopefully won't have to

ExtractWeather - Used to establish a connection to the weather supplier and return useful data encapsulated in the 
				following objects

Weather - Base class to hold shared functionality/data amongst the different child weather types

Today - Exposes weather data for as it exists now
Historical -  Exposes weather data for as it existed historically
Range - Exposes weather data for a range of dates
TodayHistorical - Exposes Todays weather but a historical summary
"""

from functools import reduce
from operator import getitem

import requests

class ExtractWeather():

	BASE_URL = 'http://api.wunderground.com/api'

	FEATURE_URL_MAP = {
					'today': 'conditions',
					'date': 'history_',
					'date_range': 'planner_',
					'almanac': 'almanac',
					}

	FEATURE_KEY_MAP = {
						'today': 'current_observation',
						'date': 'history',
						'date_range': 'trip',
						'almanac': 'almanac',
						}

	def __init__(self,api_key):

		self.api_key = api_key

	def for_today(self,state_code,city):
		"""
		state_code: string: two letter abbv for the state
		city: string: city name
		"""
		#'http://api.wunderground.com/api/Your_Key/conditions/q/CA/San_Francisco.json'
		response = self._make_request(
						type(self).FEATURE_URL_MAP['today'],
						state_code,
						city)

		feature_key = type(self).FEATURE_KEY_MAP['today']
		if feature_key in response:
			return Today(response[feature_key])

	def for_today_historical(self,state_code,city):
		"""
		state_code: string: two letter abbv for the state
		city: string: city name
		"""
		#'http://api.wunderground.com/api/Your_Key/almanac/q/CA/San_Francisco.json'
		response = self._make_request(
						type(self).FEATURE_URL_MAP['almanac'],
						state_code,
						city)

		feature_key = type(self).FEATURE_KEY_MAP['almanac']
		if feature_key in response:
			return TodayHistorical(response[feature_key])

	def for_historical_date(self,date,state_code,city):
		"""
		date: string: YYYYMMDD format
		state_code: string: two letter abbv for the state
		city: string: city name
		"""
		# http://api.wunderground.com/api/Your_Key/history_YYYYMMDD/q/CA/San_Francisco.json
		response = self._make_request(
						['{}{}'.format(type(self).FEATURE_URL_MAP['date'],date)],
						state_code,
						city)

		feature_key = type(self).FEATURE_KEY_MAP['date']
		if feature_key in response:
			return Historical(response[feature_key])

	def for_date_range(self,date_range,state_code,city):
		"""
		date_range: string: MMDDMMDD format
		state_code: string: two letter abbv for the state
		city: string: city name
		"""
		# http://api.wunderground.com/api/Your_Key/planner_MMDDMMDD/q/CA/San_Francisco.json
		response = self._make_request(
						['{}{}'.format(type(self).FEATURE_URL_MAP['date_range'],date_range)],
						state_code,
						city)

		feature_key = type(self).FEATURE_KEY_MAP['date_range']
		if feature_key in response:
			return Range(response[feature_key])

	def for_features(self,state_code,city,today=False,date=None,date_range=None,today_historical=False):
		"""
		state_code: string: two letter abbv for the state
		city: string: city name
		today: bool: True to query for current conditions
		date: string: YYYYMMDD format
		date_range: string: MMDDMMDD format
		today_historical: bool: True to query for historical summary for today

		feature specific objects are returned in the following order. They exist
		in the list if the criteria to have the feature calculated is supplied

		Returns: [today,historical,range] a variable sized list as features are supplied
					or None in each offset if the data was requested but not able to be calculated
		"""
		query_codes = []
		weather_features = []

		# determine query codes
		if today:
			query_codes.append(type(self).FEATURE_URL_MAP['today'])
		if date:
			query_codes.append(type(self).FEATURE_URL_MAP['date']+str(date))
		if date_range:
			query_codes.append(type(self).FEATURE_URL_MAP['date_range']+str(date_range))
		if today_historical:
			query_codes.append(type(self).FEATURE_URL_MAP['almanac'])

		# make request
		response = self._make_request(query_codes,state_code,city)

		# handle response and return vals
		if today:
			feature_key = type(self).FEATURE_KEY_MAP['today']
			if feature_key in response:
				weather_features.append(Today(response[feature_key]))
			else:
				weather_features.append(None)
		if date:
			feature_key = type(self).FEATURE_KEY_MAP['date']
			if feature_key in response:
				weather_features.append(Historical(response[feature_key]))
			else:
				weather_features.append(None)
		if date_range:
			feature_key = type(self).FEATURE_KEY_MAP['date_range']
			if feature_key in response:
				weather_features.append(Range(response[feature_key]))
			else:
				weather_features.append(None)
		if today_historical:
			feature_key = type(self).FEATURE_KEY_MAP['almanac']
			if feature_key in response:
				weather_features.append(TodayHistorical(response[feature_key]))
			else:
				weather_features.append(None)

		return weather_features


	def _make_request(self,query_codes,state_code,city):

		resource_url = '{}/{}/{}/q/{}/{}.json'.format(
							type(self).BASE_URL,
							self.api_key,
							'/'.join(query_codes),
							state_code,
							city.replace(' ','_'))
		return requests.get(resource_url).json()

class Weather():

	def __init__(self,data):

		self.data = data

	def extract_value(self,keys):

		try: 
			value = reduce(getitem,keys,self.data)
			return value
		except KeyError:
			pass
		else:
			return None

class Today(Weather):

	def __init__(self,data,*args,**kwargs):
		super(Today,self).__init__(data,*args,**kwargs)
		pass

	@property
	def temp_f(self):

		if self.data:
			return self.extract_value(['temp_f'])

	@property
	def temp_c(self):

		if self.data:
			return self.extract_value(['temp_c'])

	@property
	def temp_pretty(self):

		if self.data:
			return self.extract_value(['temperature_string'])

	@property
	def weather(self):

		if self.data:
			return self.extract_value(['weather'])

class TodayHistorical(Weather):

	def __init__(self,data,*args,**kwargs):
		super(TodayHistorical,self).__init__(data,*args,**kwargs)
		pass

	@property
	def high_avg_temp_f(self):

		if self.data:
			return self.extract_value(['temp_high','normal','F'])

	@property
	def high_avg_temp_c(self):

		if self.data:
			return self.extract_value(['temp_high','normal','C'])

	@property
	def low_avg_temp_f(self):

		if self.data:
			return self.extract_value(['temp_low','normal','F'])

	@property
	def low_avg_temp_c(self):

		if self.data:
			return self.extract_value(['temp_low','normal','C'])

class Historical(Weather):

	def __init__(self,data,*args,**kwargs):
		super(Historical,self).__init__(data,*args,**kwargs)
		pass

	@property
	def temp_f(self):

		if self.data:
			return self.extract_value(['dailysummary',0,'meantempi'])

	@property
	def temp_c(self):

		if self.data:
			return self.extract_value(['dailysummary',0,'meantempm'])


class Range(Weather):

	def __init__(self,data,*args,**kwargs):
		super(Range,self).__init__(data,*args,**kwargs)
		pass

	@property
	def high_avg_temp_f(self):

		if self.data:
			return self.extract_value(['temp_high','avg','F'])

	@property
	def high_avg_temp_c(self):

		if self.data:
			return self.extract_value(['temp_high','avg','C'])

	@property
	def low_avg_temp_f(self):

		if self.data:
			return self.extract_value(['temp_low','avg','F'])

	@property
	def low_avg_temp_c(self):

		if self.data:
			return self.extract_value(['temp_low','avg','C'])