from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from booking.models import Desk, BasePricePeriod, BasePrice


def login(request):
    desk_list = Desk.objects.all()
    context = {'desk_list': desk_list}
    return render(request, 'booking/login.html', context)

def book_desk(request, desk_id):
    desk = get_object_or_404(Desk, pk=desk_id)
    return render(request, 'booking/desk_detail.html', {'desk': desk})

def register(request):
    return HttpResponse("register page.")

def index(request):
    return HttpResponse("main page.")

def search_desk(request):
    return render(request, 'booking/search_desk.html')

def search_room(request):
    return HttpResponse("search for a room page.")

def results(request):
    try:
        hour_from = request.GET['hour_from']
        hour_to = request.GET['hour_to']
        date_from = request.GET['date_from']
        date_to = request.GET['date_to']
    except (KeyError, Desk.DoesNotExist):
        # Redisplay the search form.
        return render(request, 'booking/search_desk.html', {
            'error_message': "Please fill in all the data.",
            })
    else:
        desks = BasePricePeriod.objects.filter(from_date__lt=date_from, to_date__gte=date_to)
        for d in desks:
            price[d] = BasePrice.objects.filter(pk=d.base_price)
            # cośtam policz to no.
        return HttpResponse((d, price[d]) for d in desks)

def my_reservations(request):
    return HttpResponse("manage reservations.")