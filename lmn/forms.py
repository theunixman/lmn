from django import forms
from .models import Note, UserInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class VenueSearchForm(forms.Form):
    search_name = forms.CharField(label='Venue Name', max_length=200)


class ArtistSearchForm(forms.Form):
    search_name = forms.CharField(label='Artist Name', max_length=200)


class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'picture', 'text')

    # Checks picture size
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        kb_limit = 1024 * 1024
        if picture:
            if picture.size > kb_limit:
                raise ValidationError("Image file is too large ( > 1mb)")
        return picture

    # Checks title validation
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError('Please enter a title for your note!')

        return title

    # Checks that there is input in txt
    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise ValidationError('Please enter a few lines about your experience!')

        return text


# ***Both Julie and I wrote this code.
class UserEditForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    profile_photo = forms.ImageField(widget=forms.FileInput(attrs={"id": "id_file"}), label='Profile Photo', required=False)
    x = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={"id": "id_x"}))
    y = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={"id": "id_y"}))
    width = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={"id": "id_width"}))
    height = forms.FloatField(required=False, widget=forms.HiddenInput(attrs={"id": "id_height"}))
    about_me = forms.CharField(label='About Me', widget=forms.Textarea)
# ***
    


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_username(self):

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('Please enter a username')

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Please enter an email address')

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email



    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.userinfo = UserInfo()

        if commit:
            user.save()

        return user
