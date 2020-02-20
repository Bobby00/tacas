from django.db import models
from django.template.defaultfilters import slugify
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

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.description, safe_mode='escape'))


class AnalysisPost(models.Model):
	message = models.TextField(max_length=4000)
	analysis_article = models.ForeignKey(AnalysisArticle, related_name='analysis_posts', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='analysis_posts', on_delete=models.CASCADE)
	updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.created_by)

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message, safe_mode='escape'))


class AnalysisComment(models.Model):
    message = models.TextField(max_length=4000)
    analysis_post = models.ForeignKey(AnalysisPost, related_name='analysis_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='analysis_comments', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_by)

    def save(self, *args, **kwargs):
        self.url= slugify(self.analysis_post)
        super(AnalysisComment, self).save(*args, **kwargs)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class AnalysisComment2(models.Model):
    message = models.TextField(max_length=4000)
    analysis_comment = models.ForeignKey(AnalysisComment, related_name='analysis_comments2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='analysis_comments2', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_by)

    def save(self, *args, **kwargs):
        self.url= slugify(self.article_comment)
        super(ArticleComment2, self).save(*args, **kwargs)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
