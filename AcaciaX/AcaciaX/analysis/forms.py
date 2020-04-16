from django import forms
from .models import AnalysisArticle, AnalysisPost, AnalysisComment, AnalysisComment2


ANALYSIS_CATEGORY = (
		('COMMODITIES WEEKLY', 'Commodities weekly'),
	)

class NewAnalysisForm(forms.ModelForm):
	title = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Write the analysis piece title',
				'class' : 'bder-cstm-clr'
			}),
			max_length=120,
			label='Analysis title'
	)
	category = forms.ChoiceField(choices=ANALYSIS_CATEGORY)
	description = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'rows': 5, 
				'placeholder': 'What is on your mind?',
				'class' : 'bder-cstm-clr'}
		),
		max_length=4000,
		label='message body'
		
	)
	class Meta:
		model = AnalysisArticle
		fields = ['title', 'category', 'description', 'image']

class PostForm(forms.ModelForm):
    class Meta:
        model = AnalysisPost
        fields = ['message', ]

class AnalysisCommentForm(forms.ModelForm):
    class Meta:
        model = AnalysisComment
        fields = ['message', ]

class AnalysisCommentForm2(forms.ModelForm):
    class Meta:
        model = AnalysisComment2
        fields = ['message', ]