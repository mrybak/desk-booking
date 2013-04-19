from django.http import HttpResponse

def login(request):
    return HttpResponse("login page.")

def register(request):
    return HttpResponse("register page.")

def index(request):
    return HttpResponse("main page (after login).")

def search_desk(request):
    return HttpResponse("search for a desk page.")

def search_room(request):
    return HttpResponse("search for a room page.")

def results(request):
    return HttpResponse("results page.")

def my_reservations(request):
    return HttpResponse("manage reservations.")