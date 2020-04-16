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

    def get_topic_list(self):
        return Topic.objects.filter(category=self).order_by('-last_updated').all()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)


class Post(models.Model):
    message = models.TextField(max_length=10000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.url= slugify(self.topic)
        super(Post, self).save(*args, **kwargs)

    def get_page_count(self):
        count = self.comments.count()
        pages = count / 20
        return math.ceil(pages)

    def get_topic_participants(self):
        return Post.objects.filter(topic=self)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class Comment(models.Model):
    message = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def get_page_count(self):
        count = self.comments2.count()
        pages = count / 20
        return math.ceil(pages)

    def save(self, *args, **kwargs):
        self.url= slugify(self.post)
        super(Comment, self).save(*args, **kwargs)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

class Comment2(models.Model):
    message = models.TextField(max_length=10000)
    comment = models.ForeignKey(Comment, related_name='comments2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments2', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.url= slugify(self.comment)
        super(Comment2, self).save(*args, **kwargs)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


PREFERENCE_LIKE = 1
PREFERENCE_DISLIKE = -1

PREFERENCES = (
    (PREFERENCE_LIKE, 'like'),
    (PREFERENCE_DISLIKE, 'dislike'),
)


class Preference(models.Model):
    user = models.ForeignKey(User, related_name='preference', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='preference', on_delete=models.CASCADE)
    value = models.IntegerField(choices=PREFERENCES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post")
