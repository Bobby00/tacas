from django.db import models
from django.contrib.auth.models import User

class AnalysisCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class AnalysisArticle(models.Model):
	title = models.CharField(max_length=255)
	photo = models.ImageField()
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
	news_category = models.ForeignKey(AnalysisCategory, related_name='analysis', on_delete=models.CASCADE)
	starter = models.ForeignKey(User, related_name='analysis', on_delete=models.CASCADE)


class AnalysisPost(models.Model):
    message = models.TextField(max_length=4000)
    analysis_article = models.ForeignKey(AnalysisArticle, related_name='analysis_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='analysis_posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
