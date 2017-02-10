from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone


@login_required
def new_note(request, show_pk):

    show = Show.objects.get(pk=show_pk)

    if request.method == 'POST' :

        form = NewNoteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            note = form.save(commit=False);
            note.user = request.user
            note.show = show
            note.posted_date = timezone.now()
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form' : form , 'show':show})


##Venue stuff

def venue_list(request):

    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        #search for this venue, display results
        venues = Venue.objects.filter(name__contains=search_name).order_by('name')
    else :
        venues = Venue.objects.all().order_by('name')   # Todo paginate

    return render(request, 'lmn/venues/venue_list.html', { 'venues' : venues, 'form':form, 'search_term' : search_name })



def artists_at_venue(request, venue_pk):   # pk = venue_pk

    ''' Get all of the artists who have played a show at the venue with pk provided '''

    shows = Show.objects.filter(venue=venue_pk).order_by('show_date').reverse() # most recent first
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', {'venue' : venue, 'shows' :shows})



def venues_for_artist(request, artist_pk):   # pk = artist_pk

    ''' Get all of the venues where this artist has played a show '''

    shows = Show.objects.filter(artist=artist_pk).order_by('show_date').reverse() # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', {'artist' : artist, 'shows' :shows})


def venue_detail(request, venue_pk):
    venue = Venue.objects.get(pk=venue_pk);
    return render(request, 'lmn/venues/venue_detail.html' , {'venue' : venue})


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__contains=search_name).order_by('name')
    else:
        artists = Artist.objects.all().order_by('name')

    return render(request, 'lmn/artists/artist_list.html', {'artists':artists, 'form':form, 'search_term':search_name})


def artist_detail(request, artist_pk):
    artist = Artist.objects.get(pk=pk);
    return render(request, 'lmn/artists/artist_detail.html' , {'artist' : artist})


def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()
    return render(request, 'lmn/notes/note_list.html', {'notes':notes})


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    return render(request, 'lmn/notes/note_list.html', {'show': show, 'notes':notes } )



def note_detail(request, note_pk):
    note = Note.objects.get(pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , {'note' : note })


def homepage(request):
    return render(request, 'lmn/home.html')



def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk)
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'notes' : usernotes })



@login_required
def my_user_profile(request):
    # TODO - editable version for logged-in user to edit own profile
    return redirect('lmn:user_profile', user_pk=request.user.pk)



def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )
