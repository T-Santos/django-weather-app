"""
Used to gather the 'top N' U.S. cities by population. 
Returns: list of tuples in the form (city name, state name, state abbr)
"""

# 3rd party modules
import requests
from bs4 import BeautifulSoup

# local modules
from .state_dicts import state_name_dict

def extract_locations(top_N = None):

	# Globals and magic numbers
	SOURCE_URL = 'https://simple.wikipedia.org/wiki/List_of_United_States_cities_by_population'
	# would ideally want to extract from the following location
	# https://simple.wikipedia.org/w/api.php?format=json&action=query&titles=List_of_United_States_cities_by_population&prop=revisions&rvprop=content
	
	CITY_OFFSET = 1 # <td> cell offset of city name
	STATE_OFFSET = 2 # <td> cell number of state name
	TABLE_HEADER_ROW_COUNT = 1 # number of rows (<tr>'s) the source's table header takes up 

	locations = []

	# make the request and get interesting contents of page
	page = requests.get(SOURCE_URL).text
	page_contents = BeautifulSoup(page,'html.parser')
	table = page_contents.find("table",class_='wikitable')

	# used to skip over header row
	table_rows = table.find_all('tr')[TABLE_HEADER_ROW_COUNT:(top_N+TABLE_HEADER_ROW_COUNT)]

	for row in table_rows:

		# get cells in each row
		cells = row.find_all('td')

		# capture city
		city = cells[CITY_OFFSET].a.string

		# capture state and use the following to convert 
		# states such as Hawai'i to Hawaii
		state = cells[STATE_OFFSET].a.string.replace("'",'')

		# do a lookup to get the state's letters
		state_letters = state_name_dict[state]

		locations.append((city,state,state_letters))

	return locations