from django.shortcuts import render, redirect
from .models import Venue, Artist, Note, Show, UserInfo
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, Http404
from PIL import Image
import io


def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if hasattr(user, 'userinfo') and hasattr(user.userinfo, 'about_me'):
        about_me = user.userinfo.about_me
    else:
        about_me = 'This user has not finished creating their profile yet.'
    usernotes = Note.objects.filter(user=user).order_by('posted_date').reverse()
    return render(request, 'lmn/users/user_profile.html', {'user': user, 'notes': usernotes, 'about_me': about_me})


# ***Julie's code
def user_profile_photo(request, user_pk):
    user = User.objects.get(pk=user_pk)

    uinfo = user.userinfo
    if uinfo is None:
        return Http404("No such photo.")

    photo = uinfo.user_photo
    ctype = uinfo.user_photo_type
    return HttpResponse(photo, content_type=ctype)
# ***

def crop_photo(cleaned_data, photo):
       
        x = cleaned_data.get('x')
        y = cleaned_data.get('y')
        w = cleaned_data.get('width')
        h = cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        buffer = io.BytesIO()
        resized_image.save(buffer, 'JPEG')

        return buffer.getvalue()
        


@login_required
def my_user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get("first_name", False)
            user.last_name = form.cleaned_data.get("last_name", False)
            user.email = form.cleaned_data.get("email", False)
            about_me = form.cleaned_data.get("about_me", False)
            photo = request.FILES.get("profile_photo", False)

            user.userinfo.about_me = about_me
            x = form.cleaned_data.get('x', None)
            if x is not None and hasattr(photo, 'content_type') and photo.content_type is not None:
           
# ***Julie wrote this code.
                user.userinfo.user_photo_type = photo.content_type
                user.userinfo.user_photo_name = photo.name
                photo = crop_photo(form.cleaned_data,photo)
                user.userinfo.user_photo = photo
# ***

            user.save()
            user.userinfo.save()

    if hasattr(user, 'userinfo') and user.userinfo is not None:
        about_me = user.userinfo.about_me
        photo = user.userinfo.user_photo
    else:
        user.userinfo = UserInfo()
        about_me = ""
        photo = 0b000000
        user.save()
        user.userinfo.save()

# *** Both Julie and I wrote this code.
    form = UserEditForm({"first_name": user.first_name,
                         "last_name": user.last_name,
                         "email": user.email,
                         "about_me": about_me,
                         "profile photo": photo})
# ***
    return render(request, 'lmn/users/my_user_profile.html', {'form': form, 'user': user})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('lmn:my_user_profile')

        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', {'form': form, 'message': message})
    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
