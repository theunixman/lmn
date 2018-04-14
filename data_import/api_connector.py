from data_import.update_scheduler import scheduler
import requests

scheduler = scheduler()
# @scheduler.scheduled_job(trigger='cron', day='*', hour=0, minute=1, second=1, timezone='US/Central')
@scheduler.scheduled_job(trigger='interval', seconds=45)
def update_db_from_api():
    update_data = requests.get("http://localhost:5000/events").json()
    fetch_shows(update_data)

def fetch_shows(show_data):
    list_of_shows = []
    for show in show_data:
        print(show)
    #     new_show = Show(show.sk_id, show.artist, show.show_date, show.venue, None)
    #     list_of_shows.append(new_show)
    # return list_of_shows

def fetch_artist(artist_name):
    pass

def fetch_venue(venue_name):
    pass

def check_db_artist_exists(artist_objects_list):
    pass

def check_db_venue_exists(venue_objects_list):
    pass

def db_add_artist(artist):
    pass

def db_add_venue(venue):
    pass

def db_add_show(show):
    pass

