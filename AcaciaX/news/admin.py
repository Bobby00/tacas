from django.contrib import admin

from .models import NewsArticle, NewsPost

admin.site.register(NewsArticle)
admin.site.register(NewsPost)
