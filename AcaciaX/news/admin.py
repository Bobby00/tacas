from django.contrib import admin

from .models import NewsCategory, NewsArticle

admin.site.register(NewsCategory)
admin.site.register(NewsArticle)
