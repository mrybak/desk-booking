# coding=utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView
from booking.models import Desk, BasePricePeriod, BasePrice, ReservationPeriod, Room, Reservation


def login_view(request):
    return render(request, 'booking/login.html')

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/booking/')

def verify(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return redirect('/booking/index/')
        else:
            # Return a 'disabled account' error message
            return redirect('/booking/')
    else:
        # Return an 'invalid login' error message
        return redirect('/booking/')

def register(request):
    return render(request, 'booking/register.html')

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    re_password = request.POST['re_password']
    if (password == re_password):
        user = User.objects.create_user(username, username, password)
        return redirect('/booking/index/')
    else:
        # Return an error message
        return redirect('/booking/register')

@login_required
def index(request):
    return render(request, 'booking/index.html')

@login_required
def search_desk(request):
    return render(request, 'booking/search_desk.html')

@login_required
def search_room(request):
    return render(request, 'booking/search_room.html')

@login_required
def book_desk(request):
    desk_id = request.POST['desk_id']
    r = Reservation()
    r.user = request.user
    r.desk = Desk.objects.get(pk = desk_id)
    # ugly hack
    r.period_id = 1
    r.save()
    return HttpResponse('ok')

@login_required
def book_room(request):
    room_id = request.POST['room_id']
    r = Reservation()
    r.user = request.user
    # change
    r.desk = Desk.objects.get(pk = room_id)
    # ugly hack
    r.period_id = 1
    r.save()
    return HttpResponse('ok' + str(request.user.id))

class DeskList(ListView):
    template_name = 'booking/desk_results.html'
    def get_queryset(self):
        return Desk.objects.all()


    # try:
    #     hour_from = request.GET['hour_from']
    #     hour_to = request.GET['hour_to']
    #     date_from = request.GET['date_from']
    #     date_to = request.GET['date_to']
    # except (KeyError, Desk.DoesNotExist):
        # Redisplay the search form.
        # return render(request, 'booking/search_desk.html', {
        #     'error_message': "Please fill in all the data.",
        #     })
    # else:
        # desks = BasePricePeriod.objects.filter(from_date__lt=date_from, to_date__gte=date_to)
        # for d in desks:
        #     price[d] = BasePrice.objects.filter(pk=d.base_price)
            # cośtam policz to no.
        # return HttpResponse((d, price[d]) for d in desks)

class RoomList(ListView):
    template_name = 'booking/room_results.html'
    def get_queryset(self):
        return Room.objects.all()

class ReservationList(ListView):
    template_name = 'booking/my_reservations.html'
    def get_queryset(self):
        return Reservation.objects.filter(user = self.request.user)

@login_required
def cancel_reservation(request):
    resv_id = request.POST['resv_id']
    r = Reservation.objects.get(pk = resv_id)
    r.delete()
    return HttpResponse('ok')
