from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show, User, UserProfile
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserProfileEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone



def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    userP= UserProfile.objects.get(user = user)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'userProfile': userP, 'notes' : usernotes })



@login_required
def my_user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    userP= UserProfile.objects.get(user = user)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    form = UserProfileEditForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            userPNone = form.save(commit=False)
            userP.about = userPNone.about
            userP.save()
            return render(request, 'lmn/users/user_profile.html', {'user' : user , 'userProfile':userP, 'notes' : usernotes })
        else:
            form = UserProfileEditForm(instance=userP)
            message = 'Check the data you entered. Data did not save'
            return render(request, 'lmn/users/my_user_profile.html', {'form': form, 'user' : user , 'userProfile':userP , 'message':message} )
    else:
        form = UserProfileEditForm(instance=userP)
        return render(request, 'lmn/users/my_user_profile.html', {'form': form, 'user' : user , 'userProfile':userP } )




def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            if request.user.is_authenticated():  # If userprofile object has a user object property
                userP = UserProfile(user = user, about = '', joined_date=timezone.now())

                userP.save()
                return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )


def logout_view(request):
    response = logout(request)
    message = 'You have been logged out\n Goodbye!'
    return render(request, 'registration/logout.html', {'message':message})
