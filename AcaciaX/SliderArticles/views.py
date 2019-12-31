from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from .models import SliderArticle, ArticlePost
from analysis.models import AnalysisArticle

from SliderArticles.forms import PostForm

class ArticleListView(ListView):
    model = SliderArticle
    context_object_name = 'article_list'
    template_name = 'article.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['analysis_objects'] = AnalysisArticle.objects.all()
        return context

def article_posts(request, article_pk):
    analysis_objects = AnalysisArticle.objects.all()
    article = get_object_or_404(SliderArticle, pk=article_pk)
    context = {
        'analysis_objects': analysis_objects,
        'article' : article
    }
    return render(request, 'article_post.html', context)


@login_required
def reply_news_article(request, article_pk):
    article = get_object_or_404(SliderArticle, pk=article_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.article = article
            post.created_by = request.user
            post.save()
            return redirect('article_posts', article_pk=article_pk)
    else:
        form = PostForm()
    return render(request, 'reply_article.html', {'article': article, 'form': form})
