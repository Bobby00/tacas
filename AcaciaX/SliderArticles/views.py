from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import DeleteView
from .models import SliderArticle, ArticlePost, ArticleComment, ArticleComment2
from analysis.models import AnalysisArticle

from SliderArticles.forms import NewArticleForm, ArticlePostForm, ArticleCommentForm, ArticleCommentForm2


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
def new_article(request):
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.starter = request.user
            article.save()
            return redirect('article')  # TODO: redirect to the created topic page
    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {'form': form})


@superuser_required()
@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(UpdateView):
    model = SliderArticle
    fields = ('title','category','description','image' )
    template_name = 'edit_article.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(starter=self.request.user)

    def form_valid(self, form):
        article = form.save(commit=False)
        article.updated_by = self.request.user
        article.updated_at = timezone.now()
        article.save()
        return redirect('article', article_pk=article.pk)

@superuser_required()
class ArticleDelete(DeleteView):
    model = SliderArticle
    success_url = reverse_lazy('article')


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

@login_required
def reply_article(request, article_pk):
    article = get_object_or_404(SliderArticle, pk=article_pk)
    if request.method == 'POST':
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.article = article
            post.created_by = request.user
            post.save()
            return redirect('article_posts', article_pk=article_pk)
    else:
        form = ArticlePostForm()
    return render(request, 'reply_article.html', {'article': article, 'form': form})


@login_required
def reply_article_post(request, article_pk, article_post_pk):
    article_post = get_object_or_404(ArticlePost, pk=article_post_pk)
    if request.method == 'POST':
        form = ArticleCommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.article_post = article_post
            post.created_by = request.user
            post.save()
            return redirect('article_posts', article_pk=article_pk)
    else:
        form = ArticleCommentForm()
    return render(request, 'reply_article_post.html', {'article_post': article_post, 'form': form})



@login_required
def article_post_delete(request, article_pk, article_post_pk):
    article_post = get_object_or_404(ArticlePost, pk=article_post_pk)
    creator = article_post.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        article_post.delete()
        return redirect('article_posts', article_pk=article_pk)
    
    context= {'article_post': article_post,
              'creator': creator,
              }

# class ArticlePostDelete(DeleteView):
#     model = ArticlePost
#     slug_field = 'article_post_slug'
#     success_url = reverse_lazy('article_posts')


@login_required
def reply_article_comment(request, article_pk, article_post_pk, article_comment_pk):
    article_comment = get_object_or_404(ArticleComment, pk=article_comment_pk)
    if request.method == 'POST':
        form = ArticleCommentForm2(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_comment = article_comment
            comment.created_by = request.user
            comment.save()
            return redirect('article_posts', article_pk=article_pk)
    else:
        form = ArticleCommentForm2()
    return render(request, 'reply_article_comment.html', {'article_comment': article_comment, 'form': form})


@login_required
def article_comment_delete(request, article_pk, article_post_pk, article_comment_pk):
    article_comment = get_object_or_404(ArticleComment, pk=article_comment_pk)
    creator = article_comment.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        article_comment.delete()
        return redirect('article_posts', article_pk=article_pk)
    
    context= {'article_comment': article_comment,
              'creator': creator,
              }


@login_required
def article_comment2_delete(request, article_pk, article_post_pk, article_comment_pk, article_comment2_pk):
    article_comment2 = get_object_or_404(ArticleComment2, pk=article_comment2_pk)
    creator = article_comment2.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        article_comment2.delete()
        return redirect('article_posts', article_pk=article_pk)
    
    context= {'article_comment2': article_comment2,
              'creator': creator,
              }


def article_posts(request, article_pk):
    analysis_objects = AnalysisArticle.objects.all()
    article = get_object_or_404(SliderArticle, pk=article_pk)
    if request.method == 'POST':
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.article = article
            post.created_by = request.user
            post.save()
    else:
        form = ArticlePostForm()
    context = {
        'analysis_objects': analysis_objects,
        'article' : article,
        'form':form
    }
    return render(request, 'article_post.html', context)


@method_decorator(login_required, name='dispatch')
class ArticlePostUpdateView(UpdateView):
    model = ArticlePost
    fields = ('message', )
    template_name = 'edit_article_post.html'
    pk_url_kwarg = 'article_post_pk'
    context_object_name = 'article_post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        article_post = form.save(commit=False)
        article_post.updated_by = self.request.user
        article_post.updated_at = timezone.now()
        article_post.save()
        return redirect('article_posts', article_pk=article_post.article.pk)


@method_decorator(login_required, name='dispatch')
class ArticleCommentUpdateView(UpdateView):
    model = ArticleComment
    fields = ('message', )
    template_name = 'edit_article_comment.html'
    pk_url_kwarg = 'article_comment_pk'
    context_object_name = 'article_comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        article_comment = form.save(commit=False)
        article_comment.updated_by = self.request.user
        article_comment.updated_at = timezone.now()
        article_comment.save()
        return redirect('article_posts', article_pk=article_comment.article_post.article.pk)

@method_decorator(login_required, name='dispatch')
class ArticleComment2UpdateView(UpdateView):
    model = ArticleComment2
    fields = ('message', )
    template_name = 'edit_article_comment2.html'
    pk_url_kwarg = 'article_comment2_pk'
    context_object_name = 'article_comment2'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        article_comment2 = form.save(commit=False)
        article_comment2.updated_by = self.request.user
        article_comment2.updated_at = timezone.now()
        article_comment2.save()
        return redirect('article_posts', article_pk=article_comment2.article_comment.article_post.article.pk)
