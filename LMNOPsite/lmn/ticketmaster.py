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
base_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey={}&stateCode=MN'


def get_dates_for_artist():

    key = 'xqbpUW8lmN8nnoX3UHO7suHosVMf8oBF'

    url = base_url.format(key)

    response = requests.get(url)

    tm_json = response.json()

    info_list = []

    try:

        for event in tm_json["_embedded"]['events']["_embedded"]['venues']:

            print(event)


        artist = tm_json["_embedded"]['events'][0]
        print(artist['url']) # ticket infor url
        venue = artist["_embedded"]['venues'][0] # Gets venue
        print(venue['name'])
        info_list.append(artist['url'])
        info_list.append(venue['name'])

        print(info_list)

        return info_list


    except Exception as e:


        return info_list
