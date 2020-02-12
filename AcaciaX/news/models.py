from django.db import models
from django.contrib.auth.models import User

from django.utils.html import mark_safe
from markdown import markdown

class NewsArticle(models.Model):
	NEWS_ARTICLE_CATEGORY = (
		('STOCK MARKET', 'STOCK MARKET'),
		('COMMODITIES', 'COMMODITIES'),
		('FUTURES', 'FUTURES'),
	)
	title = models.CharField(max_length=255)
	description = models.TextField(max_length=4000)
	category = models.CharField(max_length = 255, choices=NEWS_ARTICLE_CATEGORY, default='STOCK MARKET')
	image = models.ImageField(upload_to='news', blank=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	starter = models.ForeignKey(User, related_name='news_article', on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class NewsPost(models.Model):
	message = models.TextField(max_length=4000)
	news_article = models.ForeignKey(NewsArticle, related_name='news_posts', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='news_posts', on_delete=models.CASCADE)
	updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.created_by)

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message, safe_mode='escape'))
