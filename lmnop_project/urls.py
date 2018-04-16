"""LMNOPsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django_apscheduler.jobstores import register_events

from lmn import views_users
from lmn.models import Artist, Venue, Show

# from django.views.generic.edit import CreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),   # Admin site

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views_users.register, name='register'),

    url(r'^', include('lmn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


'''
=========================================================================
EVERYTHING BELOW HERE IS FOR THE SCHEDULER THAT AUTO-UPDATES THE DATABASE
=========================================================================
'''


def update_db_from_api() -> None:
    update_data = requests.get("http://localhost:5000/events").json()  # Address of the LMNFlask api
    fetch_shows(update_data)


scheduler = BackgroundScheduler()
scheduler.add_job(update_db_from_api, trigger='interval', seconds=3600)  # Time between calls to api
# @scheduler.scheduled_job(trigger='cron', day='*', hour=0, minute=1, second=1, timezone='US/Central')
# TODO switch the schedulers above for production
register_events(scheduler)
scheduler.start()


def fetch_shows(response_data: dict) -> None:

    for show_data in response_data:

        new_artist = None
        new_venue = None

        if verify_venue_data(show_data):
            new_venue = build_venue(show_data)
            add_venue_if_not_exists(show_data, new_venue)

        if verify_artist_data(show_data):
            new_artist = build_artist(show_data)
            add_artist_if_not_exists(show_data, new_artist)

        if new_artist is not None and new_venue is not None:
            new_show = build_show(show_data)
            add_show_if_not_exists(show_data, new_show)


def verify_venue_data(show: dict) -> bool:

    return show['venue_id'] is not None and show['venue'] != 'Unknown venue'


def verify_artist_data(show: dict) -> bool:

    return show['artist_id'] is not None and show['artist'] != 'Unknown artist'


def build_artist(show: dict) -> Artist:

    new_artist = Artist(sk_id=show['artist_id'],
                        pkey=0,
                        name=show['artist'])
    return new_artist


def build_venue(show: dict) -> Venue:

    new_venue = Venue(sk_id=show['venue_id'],
                      pkey=0,
                      name=show['venue'],
                      city=show['city'],
                      state=show['state'])
    return new_venue


def build_show(show: dict) -> Show:

    attr = clean_show_attributes(show)

    new_show = Show(pkey=0,
                    sk_id=show['sk_id'],
                    show_date=attr['show_date'],
                    artist=attr['artist'],
                    venue=attr['venue'])
    return new_show


def add_artist_if_not_exists(show: dict, new_artist: Artist) -> None:

    if not Artist.objects.filter(sk_id=show['artist_id']).exists():
        new_artist.save()


def add_venue_if_not_exists(show: dict, new_venue: Venue) -> None:

    if not Venue.objects.filter(sk_id=show['venue_id']).exists():
        new_venue.save()


def add_show_if_not_exists(show: dict, new_show: Show) -> None:

    if not Show.objects.filter(sk_id=show['sk_id']).exists():
        new_show.save()


def clean_show_attributes(show: dict) -> dict:

    artist_id = show['artist_id']
    venue_id = show['venue_id']

    artist = Artist.objects.get(sk_id=artist_id)
    venue = Venue.objects.get(sk_id=venue_id)

    show_date = show['date']

    if show_date is None:
        utc_dt = datetime.datetime.now(datetime.timezone.utc)
        dt = utc_dt.astimezone()
        show_date = dt

    return {'artist': artist, 'venue': venue, 'show_date': show_date}


