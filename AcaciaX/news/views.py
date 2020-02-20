from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView
from .models import NewsArticle, NewsPost
from analysis.models import AnalysisArticle

from news.forms import NewNewsForm, PostForm

# CUSTOM SUPERUSER CHECK FOR CBVs
def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper


@user_passes_test(lambda u: u.is_superuser)
@login_required
def new_news_article(request):
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.starter = request.user
            news.save()
            return redirect('news')  # TODO: redirect to the created topic page
    else:
        form = NewNewsForm()
    return render(request, 'new-news-article.html', {'form': form})


@superuser_required()
@method_decorator(login_required, name='dispatch')
class NewsUpdateView(UpdateView):
    model = NewsArticle
    fields = ('title','category','description','image' )
    template_name = 'edit_news.html'
    pk_url_kwarg = 'news_pk'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(starter=self.request.user)

    def form_valid(self, form):
        news = form.save(commit=False)
        news.updated_by = self.request.user
        news.updated_at = timezone.now()
        news.save()
        return redirect('news_posts', news_pk=news.pk)


@superuser_required()
class NewsDelete(DeleteView):
    model = NewsArticle
    success_url = reverse_lazy('news')


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
def news_post_delete(request, news_article_pk, news_post_pk):
    news_post = get_object_or_404(NewsPost, pk=news_post_pk)
    creator = news_post.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        news_post.delete()
        return redirect('news_posts', news_article_pk=news_article_pk)
    
    context= {'news_post': news_post,
              'creator': creator,
              }


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

