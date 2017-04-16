from django.shortcuts import render, redirect, get_object_or_404, render_to_response

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, NotesSearchForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show,  pk=show_pk)

    if request.method == 'POST':

        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():

            note = form.save(commit=False);
            if note.title and note.text:  # If note has both title and text
                note.user = request.user
                note.show = show
                note.posted_date = timezone.now()
                note.save()
                return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, r'lmn\notes\new_note.html' , { 'form' : form , 'show':show })

# user edit notes
@login_required
def edit_notes(request, pk):
    notes = get_object_or_404(Note, pk=pk)
    form = NewNoteForm(request.POST or None, request.FILES, instance=notes)
    if form.is_valid():
        notes = form.save(commit=False)
        notes.save()
        return redirect('lmn:latest_notes')
    else:
        form = NewNoteForm( instance=notes)
        return render(request, r'lmn\notes\edit.html', {'form': form})

def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()
    return render(request, r'lmn\notes\note_list.html', {'notes':notes})


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    return render(request, r'lmn\notes\note_list.html', {'show': show, 'notes':notes } )



def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, r'lmn\notes\note_detail.html' , {'note' : note })

# A method that deletes notes added by the user4
@login_required
def delete_notes(request, pk):
    notes = get_object_or_404(Note, pk=pk)
    notes.delete()
    return redirect('lmn:latest_notes')

def search_user_notes(request):

    search_name = request.GET.get('search_name')

    if search_name:
        notes = Notes.objects.filter(title__incontains=search_name).order_by('title')
    else:
        notes = ''
        notes = Note.objects.all().order_by('title')
    return render(request, r'lmn\notes\search_notes.html', {'notes': notes})
