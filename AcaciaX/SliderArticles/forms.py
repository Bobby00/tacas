from django import forms
from .models import ArticlePost, ArticleComment, ArticleComment2

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ['message', ]

class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['message', ]

class ArticleCommentForm2(forms.ModelForm):
    class Meta:
        model = ArticleComment2
        fields = ['message', ]