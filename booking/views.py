# coding=utf-8
from datetime import datetime
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView
from booking.models import Desk, BasePricePeriod, BasePrice, ReservationPeriod, Room, Reservation

log = logging.getLogger('myapp.logger')

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

def save_reservation(desk_id, period, user):
    r = Reservation()
    r.user = user
    r.desk = Desk.objects.select_for_update().get(pk = desk_id)
    period.save()
    r.period_id = period.id
    for resv in Reservation.objects.select_for_update().filter(desk__id=desk_id):
        if resv.period.intersects_with(period):
            raise Exception("Te biurko zostało już zarezerwowane przez kogoś innego")
    r.save()
    log.debug("rezerwacja: ")
    log.debug(r)

@transaction.commit_on_success
@login_required
def book_desk(request):
    try:
        save_reservation(request.POST['desk_id'], request.session.get('period'), request.user)
        return redirect('/booking/my_reservations?success=2')
    except (Exception):
        log.debug(Exception.message)
        return redirect('/booking/my_reservations?success=4')

@transaction.commit_on_success
@login_required
def book_room(request):
    try:
        period = request.session.get('period')
        room_id = request.POST['room_id']
        for desk in Desk.objects.select_for_update().filter(room__id=room_id):
            save_reservation(desk.id, period, request.user)
        return redirect('/booking/my_reservations?success=3')
    except (Exception):
        return redirect('/booking/my_reservations?success=4')

def create_reservation_period(request):
    p = ReservationPeriod()
    p.from_hour = 0 if request.GET['hour_from'] == "" else int(request.GET['hour_from'])
    p.to_hour = 24 if request.GET['hour_to'] == "" else int(request.GET['hour_to'])
    p.from_date = datetime.strptime(request.GET['date_from'], '%Y-%m-%d').date()
    p.to_date = datetime.strptime(request.GET['date_to'], '%Y-%m-%d').date()
    p.monday = request.GET.get('dayweek_0', False)
    p.tuesday = request.GET.get('dayweek_1', False)
    p.wednesday = request.GET.get('dayweek_2', False)
    p.thursday = request.GET.get('dayweek_3', False)
    p.friday = request.GET.get('dayweek_4', False)
    p.saturday = request.GET.get('dayweek_5', False)
    p.sunday = request.GET.get('dayweek_6', False)
    p.user_id = request.user.id

    return p

@login_required
def desk_results(request):
    p = create_reservation_period(request)

    log.debug('\n\n')

    price = p.get_price()
    desks = p.find_free_desks(request.GET['city']) if price >= 0 else []
    message = "Brak wolnych biurek dla podanych kryteriów wyszukiwania."
    request.session['period'] = p
    context = {
        'desks' : desks,
        'message' : message,
        'price' : price,
        'search_period' : p,
    }
    return render(request, 'booking/desk_results.html', context)


@login_required
def room_results(request):
    p = create_reservation_period(request)
    min_desks = 0 if request.GET['desks_count'] == "" else int(request.GET['desks_count'])

    log.debug('\n\n')

    price = p.get_price()
    free_room_ids = p.find_free_desks_ids(request.GET['city']) if price >= 0 else []
    occupated_room_ids = []
    rooms = Room.objects.all()
    for room in Room.objects.all():
        if not room.is_free(free_room_ids) or room.count_all_desks() < min_desks:
            occupated_room_ids.append(room.id)
    rooms = Room.objects.exclude(id__in=occupated_room_ids)
    message = "Brak wolnych pokojów dla podanych kryteriów wyszukiwania."
    request.session['period'] = p
    context = {
        'rooms': rooms,
        'message': message,
        'price' : price,
        'search_period' : p,
    }
    return render(request, 'booking/room_results.html', context)



class ReservationList(ListView):
    template_name = 'booking/my_reservations.html'
    def get_queryset(self):
        return Reservation.objects.filter(user = self.request.user)
    def get_context_data(self, **kwargs):
        context = super(ReservationList, self).get_context_data(**kwargs)
        try:
            success = self.request.GET['success']
            if success is not None:
                context['success'] = success
        except (MultiValueDictKeyError):
            pass
        return context

@login_required
def cancel_reservation(request):
    resv_id = request.POST['resv_id']
    r = Reservation.objects.get(pk = resv_id)
    if r is not None:
        r.delete()
        return redirect('/booking/my_reservations?success=1')
    else:
        return redirect('/booking/my_reservations?success=0')