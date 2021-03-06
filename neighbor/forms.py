from django import forms
from .models import Profile,Neighborhood,Business,Post
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo','name','bio')

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')

class NeighbourHoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        exclude = ('admin','occupants_count')

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('neighborhood','user')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'hood')