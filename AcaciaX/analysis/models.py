from django.db import models
from django.contrib.auth.models import User

from django.utils.html import mark_safe
from markdown import markdown

class AnalysisArticle(models.Model):
	ANALYSIS_ARTICLE_CATEGORY = (
		('COMMODITIES WEEKLY', 'COMMODITIES WEEKLY'),
	)
	title = models.CharField(max_length=255)
	description = models.TextField(max_length=4000)
	category = models.CharField(max_length=255, choices=ANALYSIS_ARTICLE_CATEGORY, default='COMMODITIES WEEKLY')
	image = models.ImageField(blank=True, upload_to='analysis')
	last_updated = models.DateTimeField(auto_now_add=True)
	starter = models.ForeignKey(User, related_name='analysis_articles', on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class AnalysisPost(models.Model):
	message = models.TextField(max_length=4000)
	analysis_article = models.ForeignKey(AnalysisArticle, related_name='analysis_posts', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='analysis_posts', on_delete=models.CASCADE)
	updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

	def __str__(self):
		return self.created_by

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message, safe_mode='escape'))
