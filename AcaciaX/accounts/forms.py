from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile

class SignUpForm(UserCreationForm):
    avatar = forms.ImageField()
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'avatar', 'email', 'password1', 'password2')

class ProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('avatar',)