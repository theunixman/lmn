from background_task import background
from django.utils import timezone
import logging
from .ticketmaster import get_next_day_events

from django.db import connection

# checks postgres to see if the background task has been added
def background_task_check():
    with connection.cursor() as cursor:
        cursor.execute("select * from background_task;")
        row = cursor.fetchone()
    return row

# start the daily task of adding events to database from ticketmaster.
@background()
def get_tommorow_events():
    get_next_day_events()
