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


    if request.method == 'GET':

        band_search = request.GET.get('search_name')

        band_results = get_dates_for_artist(band_search) # Will find the shows for the artist in MN.

    if request.method == 'POST':

        saved_show = request.POST.get('save')



    return render(request, 'lmn/database/data_entry.html', {'form':form})
