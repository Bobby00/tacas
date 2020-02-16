from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from .models import NewsArticle, NewsPost
from analysis.models import AnalysisArticle

from news.forms import PostForm

class NewsListView(ListView):
    model = NewsArticle
    context_object_name = 'news_list'
    template_name = 'news.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['analysis_objects'] = AnalysisArticle.objects.all()
        return context

def news_posts(request, news_article_pk):
    analysis_objects = AnalysisArticle.objects.all()
    news_article = get_object_or_404(NewsArticle, pk=news_article_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.news_article = news_article
            post.created_by = request.user
            post.save()
    else:
        form = PostForm()

    context = {
        'analysis_objects': analysis_objects,
        'news_article' : news_article,
        'form' : form
    }
    return render(request, 'news_post.html', context)


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

