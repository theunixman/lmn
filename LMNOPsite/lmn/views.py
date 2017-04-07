from django.shortcuts import render
from .ticketmaster import get_dates_for_artist

def homepage(request):

    return render(request, 'lmn/home.html')
