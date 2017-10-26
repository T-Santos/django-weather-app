from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'subscribe/$', views.Subscribe, name='subscribe'),
    url(r'subscribe/successful/$', views.SubscribeSuccessful, name='subscribe_successful'),
]