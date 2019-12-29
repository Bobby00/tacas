from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import NewsArticle, NewsPost

from news.forms import PostForm

def news(request):
	news_list = NewsArticle.objects.all()
	return render(request, 'news.html', {'news_list': news_list})

def news_posts(request, news_article_pk):
	news_article = get_object_or_404(NewsArticle, pk=news_article_pk)
	return render(request, 'news_post.html', {'news_article' : news_article})


@login_required
def reply_news_article(request, news_article_pk):
    news_article = get_object_or_404(NewsArticle, pk=news_article_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.news_article = news_article
            post.created_by = request.user
            post.save()
            return redirect('news_posts', news_article_pk=news_article_pk)
    else:
        form = PostForm()
    return render(request, 'reply_news_article.html', {'news_article': news_article, 'form': form})

