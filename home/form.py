from django import forms
from django.contrib.auth.models import User
from froala_editor.widgets import FroalaEditor
from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ('content',)


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
