from django.utils import timezone
from datetime import datetime, timedelta
import requests
import json
import logging
from lmn.keys import keys
import psycopg2


try:

    db = psycopg2.connect(database='lmnop', user='lmnop', password='yankees7')
    cur = db.cursor()

    # search = 'SELECT * FROM lmn_note'
    # cur.execute(search)
    # rows = cur.fetchall()
    # print(rows)

    artist = ('Norah Jones',)
    #search = 'SELECT * FROM lmn_artist WHERE name = %s'
    cur.execute('SELECT * FROM lmn_artist WHERE name=?', ('Norah Jones')) # TODO can't seem to figure out how to pass a string into query.
    rows = cur.fetchall()
    print(rows)


    # start the daily task of adding events to database from ticketmaster.
    base_url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey={}&startDateTime={}&endDateTime={}&stateCode=MN'

    key = keys['TM_KEY']

    # getting time and formatting it for ticketmaster.
    time = datetime.utcnow()
    start_time = time + timedelta(days=1) - timedelta(hours=13)
    final_start = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = time + timedelta(days=2) - timedelta(hours=13)
    final_end = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = base_url.format(key,final_start,final_end)

    response = requests.get(url)

    tm_json = response.json()

    #print(tm_json)



    # show_list = dict()
    #
    # try:
    #
    #     artist = tm_json["_embedded"]['events']
    #
    #     # Loop over json and pull relevant info.
    #     for entry in artist:
    #         for place in entry["_embedded"]['venues']:
    #             for artists in entry["_embedded"]['attractions']:
    #
    #                 artist = artists['name']
    #                 location = place['name']
    #                 day = entry["dates"]["start"]["localDate"]
    #                 time = entry["dates"]["start"]["localTime"]
    #
    #                 date_time = day + " " + time
    #
    #                 venue_list = []
    #
    #                 venue_list.append(location)
    #                 venue_list.append(date_time)
    #
    #                 show_list[artist] = venue_list
    #
    #
    #     print(show_list)
    #
    #     value_list = []
    #
    #     # loop over created dictionary and add show/artist to database.
    #     for key, value in show_list.items():
    #
    #         name = key
    #         value_list = show_list[key]
    #         location = value_list[0]
    #         date = value_list[1]
    #
    #
    #         artist_query = Artist.objects.filter(name = name)
    #         venue_query = Venue.objects.filter(name = location)
    #         print(artist_query)
    #
    #         # two checks to see if artist or venue don;t exist in database
    #         if not artist_query:
    #
    #             #print("no artist found")
    #             artist = Artist.objects.create(name = name)
    #
    #         artist_query = Artist.objects.filter(name = name)
    #
    #         show_query = Show.objects.filter(show_date = date).filter(artist = artist_query[0]).filter(venue = venue_query[0])
    #
    #         # if the show hasn't been created.
    #         if not show_query:
    #
    #             entry = Show.objects.create(show_date = date, artist = artist_query[0], venue = venue_query[0])
    #
    #
    #
    # except Exception as e:
    #
    #     logging.exception("Problem!")

except Exception as e:
    logging.exception('problem connecting toi database.')
