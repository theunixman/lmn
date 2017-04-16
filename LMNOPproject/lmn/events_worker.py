from background_task import background
from django.utils import timezone
import logging
from .ticketmaster import get_next_day_events

from django.db import connection

def background_task_check():
    with connection.cursor() as cursor:
        cursor.execute("select * from background_task;")
        row = cursor.fetchone()
    return row

@background()
def get_tommorow_events():
    get_next_day_events()
