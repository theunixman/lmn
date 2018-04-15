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
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
# from django.views.generic.edit import CreateView
from pytz import utc

from lmn import views, views_users
from django.conf import settings
from django.conf.urls.static import static
import requests
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# from lmn.data_import.update_scheduler import scheduler
from lmn.models import Artist, Venue, Show


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


# jobstores = {
#     # 'sqlalchemy': SQLAlchemyJobStore(),
#     'django': DjangoJobStore()
# }
#
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
#
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }

# scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


# scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')

# @scheduler.scheduled_job(trigger='cron', day='*', hour=0, minute=1, second=1, timezone='US/Central')

scheduler = BackgroundScheduler()

def update_db_from_api():
    update_data = requests.get("http://localhost:5000/events").json()
    fetch_shows(update_data)


scheduler.add_job(update_db_from_api, trigger='interval', seconds=10)

def fetch_shows(show_data):

    for show in show_data:

        if show['venue_id'] is not None and show['venue'] != 'Unknown venue':
            venue = check_db_venue_exists(show)

        if show['artist_id'] is not None and show['artist'] != 'Unknown artist':
            artist = check_db_artist_exists(show)

        # db_add_show(show, venue, artist)


def fetch_artist(artist_name):
    return artist_name
    pass

def fetch_venue(venue_name):
    return venue_name
    pass

def check_db_artist_exists(show):
    print('show[artist_id]: ' + str(show['artist_id']))

    new_artist = Artist(
        sk_id=show['artist_id'],
        pkey=0,
        name=show['artist'])

    if not Artist.objects.filter(sk_id=show['artist_id']).exists():
        print('artist from show not in db...adding')
        new_artist.save()

    return new_artist

    # else:
    #     artist = Artist.objects.filter(sk_id=show['artist_id'])
    #     print('artist present in db')
    #     return artist


def check_db_venue_exists(show):
    print('show[venue_id]: ' + str(show['venue_id']))

    new_venue = Venue(
        sk_id=show['venue_id'],
        pkey=0,
        name=show['venue'],
        city=show['city'],
        state=show['state'])

    if not Venue.objects.filter(sk_id=show['venue_id']).exists():
        print('venue from show not in db...adding')

        new_venue.save()
    return new_venue
    # else:
    #     venue = Venue.objects.filter(sk_id=show['venue_id'])
    #     print('venue present in db')
    #     return venue

def db_add_artist(artist):
    return artist
    pass

def db_add_venue(venue):
    return venue
    pass

def db_add_show(show, show_venue, show_artist):

    if not Show.objects.filter(sk_id=show['sk_id']).exists():
        print('show not in db...adding')

        new_show = Show(
            pkey=0,
            sk_id=show['sk_id'],
            show_date=show['date'],
            artist=show_artist,
            venue=show_venue)
            # artist=Artist.objects.filter(sk_id=show_artist['sk_id']),
            # venue=Venue.objects.filter(sk_id=show_venue['sk_id']))

        new_show.save()

    else:
        print('show present in db')


register_events(scheduler)

scheduler.start()
