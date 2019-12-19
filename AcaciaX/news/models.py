from django.db import models
from django.contrib.auth.models import User

class NewsCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
	title = models.CharField(max_length=255)
	photo = models.ImageField()
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
	news_category = models.ForeignKey(NewsCategory, related_name='news', on_delete=models.CASCADE)
	starter = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)


class NewsPost(models.Model):
    message = models.TextField(max_length=4000)
    news_article = models.ForeignKey(NewsArticle, related_name='news_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='news_posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
