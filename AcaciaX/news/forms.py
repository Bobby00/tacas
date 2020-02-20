from django import forms
from .models import NewsArticle, NewsPost

NEWS_CATEGORY = (
		('STOCKS', 'Stocks'),
		('FUTURES', 'Futures'),
		('COMMODITIES', 'Commodities'),
	)

class NewNewsForm(forms.ModelForm):
	title = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Write the news title',
				'class' : 'bder-cstm-clr'
			}),
			max_length=120,
			label='News title'
	)
	category = forms.ChoiceField(choices=NEWS_CATEGORY)
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
		model = NewsArticle
		fields = ['title', 'category', 'description', 'image']


class PostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['message', ]