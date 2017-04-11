from django.shortcuts import render
from .ticketmaster import get_all_current_venues
from .models import Venue


def homepage(request):

    venue_check_query = Venue.objects.all()

    if not venue_check_query:

        print('empty')


    return render(request, 'lmn/home.html')
