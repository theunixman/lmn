from django.shortcuts import render
from .ticketmaster import get_dates_for_artist

def homepage(request):

    get_dates_for_artist() # This is a test for the ticketmaster, it doesn't mean anything yet and will eventually be moved.

    return render(request, 'lmn/home.html')
