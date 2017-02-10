from django.conf.urls import url
from . import views

from django.contrib.auth import views as auth_views

app_name = 'lmn'

urlpatterns = [

    url(r'^$', views.homepage, name='homepage'),

    #Venue-related
    # url(r'^venues/$', views.venue_search, name='venue_search'),
    url(r'^venues/list/$', views.venue_list, name='venue_list'),
    url(r'^venues/detail/(?P<venue_pk>\d+)/$', views.venue_detail, name='venue_detail'),
    url(r'^venues/artists_at/(?P<venue_pk>\d+)/$', views.artists_at_venue, name='artists_at_venue'),

    #Note related
    url(r'^notes/latest/$', views.latest_notes, name='latest_notes'),
    url(r'^notes/detail/(?P<note_pk>\d+)/$', views.note_detail, name='note_detail'),
    url(r'^notes/for_show/(?P<show_pk>\d+)/$', views.notes_for_show, name='notes_for_show'),
    url(r'^notes/add/(?P<show_pk>\d+)/$', views.new_note, name='new_note'),


    #Artist related
    url(r'^artists/list/$', views.artist_list, name='artist_list'),
    url(r'^artists/detail/(?P<artist_pk>\d+)/$', views.artist_list, name='artist_list'),
    url(r'^artists/venues_played/(?P<artist_pk>\d+)/$', views.venues_for_artist, name='venues_for_artist'),

    # User related
    url(r'^user/profile/(?P<user_pk>\d+)/$', views.user_profile, name='user_profile'),
    url(r'^user/profile/$', views.my_user_profile, name='my_user_profile'),

    # Login/logout/signup views are in the app-level urls.py

]
