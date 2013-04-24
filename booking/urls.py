from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from booking import views
from booking.views import ReservationList

urlpatterns = patterns('',
    url(r'^$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^auth/$', views.verify, name='verify'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^search_desk/$', views.search_desk, name='search_desk'),
    url(r'^search_room/$', views.search_room, name='search_room'),
    url(r'^results/$', views.results, name='results'),
    url(r'^my_reservations/$', login_required(ReservationList.as_view()), name="my_reservations"),
    url(r'^book_desk/(?P<desk_id>\d+)/$', views.book_desk, name='book_desk'),
    url(r'^book_room/(?P<room_id>\d+)/$', views.book_room, name='book_room'),
)