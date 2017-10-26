# django-weather-app

### start up virtual env

```
source bin/activate

python manage.py makemigrations
python manage.py makemigrations common
python manage.py makemigrations weather
python manage.py migrate

python manage.py update_states
python manage.py update_locations
```

### Optional
#### python manage.py createsuperuser

```
python manage.py runserver
```

#### to send emails to weather subscribers, do one of the following
```
export WEATHER_API_KEY=XXXXXXXXXX
python manage.py send_weather_emails [--API_KEY XXXXXX]
```
