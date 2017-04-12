from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

import requests
import json
import logging


# This is a test file for filtering out show data from Ticketmaster.
#base_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey={}&keyword={}&stateCode=MN'

# This class pulls data from ticketmaster and returns a dict of the Venues in Minnesota.
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

        for entry in artist:
            for place in entry["_embedded"]['venues']:

                location = place['name']
                city = place['city']['name']

                if location not in venue_list:

                    venue_list[location] = city


        return venue_list




    except Exception as e:

        logging.exception("Problem!")



def get_dates_for_artist(band_name):

    base_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey={}&keyword={}&stateCode=MN'

    key = 'xqbpUW8lmN8nnoX3UHO7suHosVMf8oBF'

    url = base_url.format(key, band_name)

    response = requests.get(url)

    tm_json = response.json()


    show_list = dict()


    # Error check to see if the JSON found a event in Minnesota.
    try:

        artist = tm_json["_embedded"]['events']

    except Exception as e:

        print("no band found")


    try:

        artist = tm_json["_embedded"]['events']

        for entry in artist:
            for place in entry["_embedded"]['venues']:
                for artists in entry["_embedded"]['attractions']:

                    artist = artists['name']
                    location = place['name']
                    day = entry["dates"]["start"]["localDate"]

                    venue_list = []

                    venue_list.append(location)
                    venue_list.append(day)

                    show_list[artist] = venue_list


        print(show_list)


    except Exception as e:

        logging.exception("Problem!")
