from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

        #here we created meta class so that anything that affects within the under User model
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
         # these are the fields that we want to use in forms

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
