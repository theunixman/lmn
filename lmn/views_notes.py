from django.shortcuts import render, redirect, get_object_or_404
from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':

        form = NewNoteForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            note = form.save(commit=False)
            if note.title and note.text:  # If note has both title and text
                note.user = request.user
                note.show = show
                note.picture = note.picture
                note.posted_date = timezone.now()
                note.save()
                return redirect('lmn:note_detail',
                                note_pk=note.pk)

    else:
        form = NewNoteForm()

    return render(request,
                  'lmn/notes/new_note.html',
                  {'form': form,
                   'show': show})


def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()

    paginator = Paginator(notes, 25)
    page = request.GET.get('page')

    try:
        noteset = paginator.page(page)

    except PageNotAnInteger:
        noteset = paginator.page(1)

    except EmptyPage:
        noteset = paginator.page(paginator.num_pages)

    return render(request,
                  'lmn/notes/note_list.html',
                  {'notes': notes,
                   "noteset": noteset})


def notes_for_show(request, show_pk):   # pk = show pk
    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue
    return render(request,
                  'lmn/notes/note_list.html',
                  {'show': show,
                   'notes': notes})


@login_required
def edit_notes(request, pk):
    notes = get_object_or_404(Post, pk=pk)
    if requested.method == "Post":
        form = NewNote(request.POST or None, request.FILES, instance=notes)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.save()
            return redirect('lmn:notes')
    else:
        form = NewNote( instance=notes)
    return render(request, r'lmn/notes/edit.html', {'form': form})


@login_required
def delete_notes(request, pk):
    notes = get_object_or_404(Note, pk=pk)
    notes.delete()
    return redirect('lmn:latest_notes')


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request,
                  'lmn/notes/note_detail.html',
                  {'note': note})


@login_required
def note_edit(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    show = get_object_or_404(Show, pk=note.show.pk)
    if request.method == "POST":
        form = NewNoteForm(request.POST or None, request.FILES, instance=note)
        if form.is_valid():
            note.save()
            return redirect('lmn:note_detail', pk=note.pk)

    else:
        form = NewNoteForm(instance=note)

    return render(request,
                  'lmn/notes/note_edit.html',
                  {'form': form,
                   'note': note,
                   'show': show})


@login_required
def note_delete(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    note.delete()
    return redirect('lmn:user_profile')
