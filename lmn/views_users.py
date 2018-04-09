from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show, UserInfo
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone


def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'notes' : usernotes })


@login_required
def my_user_profile(request):

    if request.method == 'POST':

        form = UserEditForm(request.POST)
        # Sees what field values have changed before saving the profile edit form
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data["user_name"]
            user.first_name = form.cleaned_data["user_first"]
            user.last_name = form.cleaned_data["user_last"]
            user.email_address = form.cleaned_data["user_email"]
            user_about_me = UserInfo(user=user, about_me=form.cleaned_data["user_about_me"])
            user_about_me.save()
            user.save()

            return redirect('lmn:homepage')
            # Prepopulate edit profile form with user's data
            return render(request, 'lmn/users/user_profile.html', {'user' : user , 'user_name' : username, 'user_first' : userfirst, 'user_last' : userlast, 'user_email': useremail, 'user_about_me': useraboutme })
            

    else:
        form = UserEditForm()
        return render(request, 'lmn/users/my_user_profile.html', {'form': form})


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('lmn:homepage')
            
        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', {'form': form, 'message': message})

    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
