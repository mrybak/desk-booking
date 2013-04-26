from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from booking import views
from booking.views import ReservationList, RoomList, DeskList

urlpatterns = patterns('',
    url(r'^$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^auth/$', views.verify, name='verify'),
    url(r'^new_user/$', views.create_user, name='create_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^search_desk/$', views.search_desk, name='search_desk'),
    url(r'^search_room/$', views.search_room, name='search_room'),
    url(r'^book_desk/$', views.book_desk, name='book_desk'),
    url(r'^book_room/$', views.book_room, name='book_room'),
    url(r'^desk_results/$', login_required(DeskList.as_view()), name='desk_results'),
    url(r'^room_results/$', login_required(RoomList.as_view()), name='room_results'),
    url(r'^cancel_reservation/$', views.cancel_reservation, name="cancel_reservation"),
    url(r'^my_reservations/$', login_required(ReservationList.as_view()), name="my_reservations"),
    url(r'^book_desk/(?P<desk_id>\d+)/$', views.book_desk, name='book_desk'),
    url(r'^book_room/(?P<room_id>\d+)/$', views.book_room, name='book_room'),
)