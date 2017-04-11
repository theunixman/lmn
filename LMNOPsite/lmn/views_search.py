from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone
from .ticketmaster import get_dates_for_artist, get_all_current_venues


def search_for_artist(request):

    form = ArtistSearchForm()
    search = request.GET.get('search_name')
    print(search)

    #get_dates_for_artist() # This is a test for the ticketmaster, it doesn't mean anything yet and will eventually be moved.


    if request.method == 'GET':

        print('need to get the query so I can search Ticketmaster.')

    #get_dates_for_artist()

    return render(request, 'lmn/database/data_entry.html', {'form':form})
