from django.http import HttpResponse
from django.shortcuts import render
from booking.models import Desk


def login(request):
    desk_list = Desk.objects.all()
    context = {'desk_list': desk_list}
    return render(request, 'booking/login.html', context)

def register(request):
    return HttpResponse("register page.")

def index(request):
    return HttpResponse("main page.")

def search_desk(request):
    return HttpResponse("search for a desk page.")

def search_room(request):
    return HttpResponse("search for a room page.")

def results(request):
    return HttpResponse("results page.")

def my_reservations(request):
    return HttpResponse("manage reservations.")