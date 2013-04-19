from django.conf.urls import patterns, include, url
from booking import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.index, name='index'),
    url(r'^search_desk/$', views.search_desk, name='search_desk'),
    url(r'^search_room/$', views.search_room, name='search_room'),
    url(r'^results/$', views.results, name='results'),
    url(r'^my_reservations$', views.my_reservations, name='my_reservations'),
)