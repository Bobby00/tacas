from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import mark_safe
from markdown import markdown

from django.contrib.auth.models import User

class SliderArticle(models.Model):
	ARTICLE_CATEGORY = (
		('FOREX', 'Forex'),
		('STOCKS', 'Stocks'),
		('FUTURES', 'Futures'),
	)
	title = models.CharField(max_length=255)
	description = models.TextField(max_length=4000)
	category = models.CharField(max_length = 255, choices=ARTICLE_CATEGORY, default='STOCK MARKET')
	image = models.ImageField(upload_to='slider', blank=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	starter = models.ForeignKey(User, related_name='article', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.description, safe_mode='escape'))

class ArticlePost(models.Model):
	message = models.TextField(max_length=4000)
	article = models.ForeignKey(SliderArticle, related_name='article_posts', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='article_posts', on_delete=models.CASCADE)
	updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.created_by)

	def save(self, *args, **kwargs):
		self.url= slugify(self.article)
		super(ArticlePost, self).save(*args, **kwargs)

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message, safe_mode='escape'))

class ArticleComment(models.Model):
    message = models.TextField(max_length=4000)
    article_post = models.ForeignKey(ArticlePost, related_name='article_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='article_comments', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_by)

    def save(self, *args, **kwargs):
        self.url= slugify(self.article_post)
        super(ArticleComment, self).save(*args, **kwargs)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class ArticleComment2(models.Model):
    message = models.TextField(max_length=4000)
    article_comment = models.ForeignKey(ArticleComment, related_name='article_comments2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='article_comments2', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_by)

    def save(self, *args, **kwargs):
        self.url= slugify(self.article_comment)
        super(ArticleComment2, self).save(*args, **kwargs)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

