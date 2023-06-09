from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']