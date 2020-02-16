from django import forms
from .models import AnalysisPost

class PostForm(forms.ModelForm):
    class Meta:
        model = AnalysisPost
        fields = ['message', ]