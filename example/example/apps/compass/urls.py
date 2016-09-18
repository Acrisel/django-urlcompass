from django.conf.urls import url
from .views import compass_main


app_name='compass'

urlpatterns = [
    url(r'^$', compass_main, name='compass'), 
     
    url(r'^(?P<page>\d+)/nextpage1', compass_main, name='nextpage1'),
    url(r'^(?P<page>\d+)/nextpage2', compass_main, name='nextpage2'),
    url(r'^(?P<page>\d+)/nextpage3', compass_main, name='nextpage3'),
    url(r'^(?P<page>\w+)/lastpage', compass_main, name='lastpage'),
               
]
