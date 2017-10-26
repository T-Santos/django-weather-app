from django.shortcuts import render, redirect # is used for template paths

from .forms import SubscribeWeather

def Subscribe(request):

	context = {}

	if request.method == "POST":
		weather_form = SubscribeWeather(request.POST)
		if weather_form.is_valid():
			weather_form.save()
			return redirect('subscribe_successful')
	else:
		weather_form = SubscribeWeather()

	context['weather_form'] = weather_form
	context['subscription_type'] = 'Weather'

	return render(request,'weather/subscribe.html',context)

def SubscribeSuccessful(request):
	context = {}
	context['subscription_type'] = 'Weather'

	return render(request,'weather/subscribe_successful.html',context)
	    

def index(request):
    return redirect('subscribe')