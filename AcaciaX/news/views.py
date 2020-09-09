from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView
from .models import NewsArticle, NewsPost, NewsComment, NewsComment2
from analysis.models import AnalysisArticle

from news.forms import NewNewsForm, PostForm, NewsCommentForm, NewsCommentForm2

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
    ordering = ['-last_updated']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['analysis_objects'] = AnalysisArticle.objects.order_by('-last_updated')
        return context

def news_posts(request, news_article_pk):
    analysis_objects = AnalysisArticle.objects.order_by('last_updated')
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


@method_decorator(login_required, name='dispatch')
class NewsPostUpdateView(UpdateView):
    model = NewsPost
    fields = ('message', )
    template_name = 'edit_news_post.html'
    pk_url_kwarg = 'news_post_pk'
    context_object_name = 'news_post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        news_post = form.save(commit=False)
        news_post.updated_by = self.request.user
        news_post.updated_at = timezone.now()
        news_post.save()
        return redirect('news_posts', news_article_pk=news_post.news_article.pk)


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


@login_required
def reply_news_post(request, news_article_pk, news_post_pk):
    news_post = get_object_or_404(NewsPost, pk=news_post_pk)
    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.news_post = news_post
            post.created_by = request.user
            post.save()
            return redirect('news_posts', news_article_pk=news_article_pk)
    else:
        form = NewsCommentForm()
    return render(request, 'reply_news_post.html', {'news_post': news_post, 'form': form})


@method_decorator(login_required, name='dispatch')
class NewsCommentUpdateView(UpdateView):
    model = NewsComment
    fields = ('message', )
    template_name = 'edit_news_comment.html'
    pk_url_kwarg = 'news_comment_pk'
    context_object_name = 'news_comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        news_comment = form.save(commit=False)
        news_comment.updated_by = self.request.user
        news_comment.updated_at = timezone.now()
        news_comment.save()
        return redirect('news_posts', news_article_pk=news_comment.news_post.news_article.pk)

@login_required
def news_comment_delete(request, news_article_pk, news_post_pk, news_comment_pk):
    news_comment = get_object_or_404(NewsComment, pk=news_comment_pk)
    creator = news_comment.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        news_comment.delete()
        return redirect('news_posts', news_article_pk=news_article_pk)
    
    context= {'news_comment': news_comment,
              'creator': creator,
              }

@login_required
def reply_news_comment(request, news_article_pk, news_post_pk, news_comment_pk):
    news_comment = get_object_or_404(NewsComment, pk=news_comment_pk)
    if request.method == 'POST':
        form = NewsCommentForm2(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news_comment = news_comment
            comment.created_by = request.user
            comment.save()
            return redirect('news_posts', news_article_pk=news_article_pk)
    else:
        form = NewsCommentForm2()
    return render(request, 'reply_news_comment.html', {'news_comment': news_comment, 'form': form})


@login_required
def news_comment2_delete(request, news_article_pk, news_post_pk, news_comment_pk, news_comment2_pk):
    news_comment2 = get_object_or_404(NewsComment2, pk=news_comment2_pk)
    creator = news_comment2.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        news_comment2.delete()
        return redirect('news_posts', news_article_pk=news_article_pk)
    
    context= {'news_comment2': news_comment2,
              'creator': creator,
              }

@method_decorator(login_required, name='dispatch')
class NewsComment2UpdateView(UpdateView):
    model = NewsComment2
    fields = ('message', )
    template_name = 'edit_news_comment2.html'
    pk_url_kwarg = 'news_comment2_pk'
    context_object_name = 'news_comment2'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        news_comment2 = form.save(commit=False)
        news_comment2.updated_by = self.request.user
        news_comment2.updated_at = timezone.now()
        news_comment2.save()
        return redirect('news_posts', news_article_pk=news_comment2.news_comment.news_post.news_article.pk)

