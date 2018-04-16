import requests
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from lmn.data_import.update_scheduler import scheduler
from lmn.models import Artist, Venue
from lmn.models import Show

scheduler = scheduler()
scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
scheduler.add_job('update_shows')
# @scheduler.scheduled_job(trigger='cron', day='*', hour=0, minute=1, second=1, timezone='US/Central')
@register_job(scheduler, trigger='interval', seconds=45, id='update_shows')
def update_db_from_api():
    update_data = requests.get("http://localhost:5000/events").json()
    fetch_shows(update_data)




def fetch_shows(show_data):
    list_of_shows = []
    for show in show_data:
        print(show)

        check_db_venue_exists(show.venue_id)

        check_db_artist_exists(show.artist_id)

        db_add_show(show)
        new_show = Show(show.sk_id, show.artist, show.show_date, show.venue, None)
        list_of_shows.append(new_show)
    return list_of_shows

def fetch_artist(artist_name):
    pass

def fetch_venue(venue_name):
    pass

def check_db_artist_exists(show):

    if not Artist.objects.filter(sk_id=show.artist_id).exists():

        new_artist = Artist(
            sk_id=show.artist_id,
            name=show.artist)

        new_artist.save()

def check_db_venue_exists(show):

    if not Venue.objects.filter(sk_id=show.venue_id).exists():

        new_venue = Venue(
            sk_id=show.venue_id,
            name=show.venue,
            city=show.city,
            state=show.state)

        new_venue.save()

def db_add_artist(artist):
    pass

def db_add_venue(venue):
    pass

def db_add_show(show):
    pass


register_events(scheduler)

scheduler.start()
