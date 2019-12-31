from django.db import models
import math
from django.utils.html import mark_safe
from django.template.defaultfilters import slugify
from markdown import markdown

from django.contrib.auth.models import User

# FORUM AND ACCOUNT MODELS

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__category=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__category=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.url= slugify(self.topic)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class Comment(models.Model):
    message = models.TextField(max_length=1000)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)


class Preference(models.Model):
    user = models.ForeignKey(User, related_name='preference', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='preference', on_delete=models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")
