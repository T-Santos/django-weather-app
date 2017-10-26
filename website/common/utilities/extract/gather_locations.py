import requests
from operator import itemgetter

def sort_value(item):

	return int(item[0])

def remove_bad_entries(result):

	if not result[0]:
		return None
	elif " city," not in result[1]:
		return None

	return True

def gather_locations():

	BASE_URL = 'https://api.census.gov/data/2016/pep/population?'

	payload = {
				'get': ','.join(['POP','GEONAME']),
				'for':'place:*',
				'DATE':9,
				}

	response = requests.get(BASE_URL,payload)

	# get the results in the right order
	results = response.json()[1:]
	filtered_results = [x for x in results if remove_bad_entries(x)]
	filtered_results.sort(key=sort_value,reverse=True)

	final_list = [x[1].split(' city, ') for x in filtered_results[:100]]

	return final_list
	
def main():
	pass


if __name__ == '__main__':
	main()