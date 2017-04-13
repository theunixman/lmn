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

    if request.method == 'POST':

        form_post = ArtistSearchForm(request.POST)

        if form_post.is_valid():

            band_search = form_post.cleaned_data['search_name']
            print(band_search)

            band_results = get_dates_for_artist(band_search) # Will find the shows for the artist in MN.

            if band_results == "entered":

                return render(request, 'lmn/database/data_entry.html', {'form': form, 'added': 'ok', 'artist_added': band_search})

            elif band_results == None:

                return render(request, 'lmn/database/data_entry.html', {'form': form,'not_found': 'ok', 'not_found': band_search})

            else:

                return render(request, 'lmn/database/data_entry.html', {'form': form,'already': 'ok', 'artist_in_database': band_search})


            return render(request, 'lmn/database/data_entry.html', {'form':form })


    return render(request, 'lmn/database/data_entry.html', {'form':form})
