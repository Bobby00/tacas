from django import forms
from .models import SliderArticle, ArticlePost, ArticleComment, ArticleComment2

ARTICLE_CATEGORY = (
		('FOREX', 'Forex'),
		('STOCKS', 'Stocks'),
		('FUTURES', 'Futures'),
	)

class NewArticleForm(forms.ModelForm):
	title = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Write the article title',
				'class' : 'bder-cstm-clr'
			}),
			max_length=120,
			label='Article title'
	)
	category = forms.ChoiceField(choices=ARTICLE_CATEGORY)
	description = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'rows': 5, 
				'placeholder': 'What is on your mind?',
				'class' : 'bder-cstm-clr'}
		),
		max_length=4000,
		label='Article body'
		
	)
	class Meta:
		model = SliderArticle
		fields = ['title', 'category', 'description', 'image']


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