from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_countries import countries

from .models import UserProfile


COUNTRY_CHOICES = tuple(countries)


class SignUpForm(UserCreationForm):

    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

class UserProfileForm(forms.ModelForm):
    phonenumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your Phonenumber',
                'class' : 'bder-cstm-clr'
            }),
        max_length=50,
        label='Phonenumber')

    location = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'class':'bder-cstm-clr'}))

    class Meta:
        model = UserProfile
        fields = ('phonenumber', 'location',)

