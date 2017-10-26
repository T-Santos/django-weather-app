"""
Run tests for logic used to support the sending weather email functionality
$ ./manage.py test weather/utilities/
"""

from weather.utilities.email import is_warmer_than_avg, is_cooler_than_avg

def run_tests():
	"""
	Run tests to ensure the is warmer, is cooler calculation are correct
	"""

	# is warmer test
	assert is_warmer_than_avg(-10,-10,5)==False,"-10,-10,5"
	assert is_warmer_than_avg(-5,-10,5)==True,"-5,-10,5"
	assert is_warmer_than_avg(0,-10,5)==True,"0,-10,5" 
	assert is_warmer_than_avg(5,-10,5)==True,"5,-10,5" 
	assert is_warmer_than_avg(10,-10,5)==True,"10,-10,5" 

	assert is_warmer_than_avg(-10,-5,5)==False,"-10,-5,5"
	assert is_warmer_than_avg(-5,-5,5)==False,"-5,-5,5"
	assert is_warmer_than_avg(0,-5,5)==True,"0,-5,5" 
	assert is_warmer_than_avg(5,-5,5)==True,"5,-5,5" 
	assert is_warmer_than_avg(10,-5,5)==True,"10,-5,5"

	assert is_warmer_than_avg(-10,0,5)==False,"-10,0,5"
	assert is_warmer_than_avg(-5,0,5)==False,"-5,0,5"
	assert is_warmer_than_avg(0,0,5)==False,"0,0,5" 
	assert is_warmer_than_avg(5,0,5)==True,"5,0,5" 
	assert is_warmer_than_avg(10,0,5)==True,"10,0,5" 

	assert is_warmer_than_avg(-10,5,5)==False,"-10,5,5"
	assert is_warmer_than_avg(-5,5,5)==False,"-5,5,5"
	assert is_warmer_than_avg(0,5,5)==False,"0,5,5" 
	assert is_warmer_than_avg(5,5,5)==False,"5,5,5" 
	assert is_warmer_than_avg(10,5,5)==True,"10,5,5" 

	assert is_warmer_than_avg(-10,10,5)==False,"-10,10,5"
	assert is_warmer_than_avg(-5,10,5)==False,"-5,10,5"
	assert is_warmer_than_avg(0,10,5)==False,"0,10,5" 
	assert is_warmer_than_avg(5,10,5)==False,"5,10,5" 
	assert is_warmer_than_avg(10,10,5)==False,"10,10,5" 

	# is cooler test
	assert is_cooler_than_avg(-10,-10,5)==False,"-10,-10,5"
	assert is_cooler_than_avg(-5,-10,5)==False,"-5,-10,5"
	assert is_cooler_than_avg(0,-10,5)==False,"0,-10,5" 
	assert is_cooler_than_avg(5,-10,5)==False,"5,-10,5" 
	assert is_cooler_than_avg(10,-10,5)==False,"10,-10,5" 

	assert is_cooler_than_avg(-10,-5,5)==True,"-10,-5,5"
	assert is_cooler_than_avg(-5,-5,5)==False,"-5,-5,5"
	assert is_cooler_than_avg(0,-5,5)==False,"0,-5,5" 
	assert is_cooler_than_avg(5,-5,5)==False,"5,-5,5" 
	assert is_cooler_than_avg(10,-5,5)==False,"10,-5,5"

	assert is_cooler_than_avg(-10,0,5)==True,"-10,0,5"
	assert is_cooler_than_avg(-5,0,5)==True,"-5,0,5"
	assert is_cooler_than_avg(0,0,5)==False,"0,0,5" 
	assert is_cooler_than_avg(5,0,5)==False,"5,0,5" 
	assert is_cooler_than_avg(10,0,5)==False,"10,0,5" 

	assert is_cooler_than_avg(-10,5,5)==True,"-10,5,5"
	assert is_cooler_than_avg(-5,5,5)==True,"-5,5,5"
	assert is_cooler_than_avg(0,5,5)==True,"0,5,5" 
	assert is_cooler_than_avg(5,5,5)==False,"5,5,5" 
	assert is_cooler_than_avg(10,5,5)==False,"10,5,5" 

	assert is_cooler_than_avg(-10,10,5)==True,"-10,10,5"
	assert is_cooler_than_avg(-5,10,5)==True,"-5,10,5"
	assert is_cooler_than_avg(0,10,5)==True,"0,10,5" 
	assert is_cooler_than_avg(5,10,5)==True,"5,10,5" 
	assert is_cooler_than_avg(10,10,5)==False,"10,10,5" 
	print("Success")

run_tests()