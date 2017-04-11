from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

import requests
import json


# This is a test file for filtering out show data from Ticketmaster.
#base_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey={}&keyword={}&stateCode=MN'

def get_all_current_venues():

    base_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey={}&size=500&stateCode=MN'

    key = 'xqbpUW8lmN8nnoX3UHO7suHosVMf8oBF'

    url = base_url.format(key)

    response = requests.get(url)

    tm_json = response.json()

    venue_list = dict()
    city_list = []


    try:

        artist = tm_json["_embedded"]['events']
        print(type(artist))

        for entry in artist:
            for place in entry["_embedded"]['venues']:

                location = place['name']
                city = place['city']['name']

                if location not in venue_list:

                    venue_list[location] = city
        

        # for key, value in venue_list.items():
        #
        #     place = key
        #     city = value
        #     state = 'MN'
        #
        #     Venue.objects.create(name = place, city = city, state = state)
        #
        #
        # print(Venue.objects.all())



    except Exception as e:

        print('problem')



def get_dates_for_artist():


    key = 'xqbpUW8lmN8nnoX3UHO7suHosVMf8oBF'

    url = base_url.format(key)

    response = requests.get(url)

    tm_json = response.json()

    venue_list = dict()
    city_list = []


    try:

        artist = tm_json["_embedded"]['events']
        print(type(artist))

        for entry in artist:
            for place in entry["_embedded"]['venues']:

                location = place['name']
                city = place['city']['name']

                if location not in venue_list:

                    venue_list[location] = city



        print(venue_list)
        print(type(venue_list))



    except Exception as e:

        print('problem')
