from django import forms
from .models import NewsPost

class PostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['message', ]