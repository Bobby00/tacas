from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView
from .models import AnalysisArticle, AnalysisPost, AnalysisComment, AnalysisComment2

from analysis.forms import NewAnalysisForm, PostForm, AnalysisCommentForm, AnalysisCommentForm2

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
def new_analysis(request):
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.starter = request.user
            analysis.save()
            return redirect('analysis')  # TODO: redirect to the created topic page
    else:
        form = NewAnalysisForm()
    return render(request, 'new-analysis.html', {'form': form})


@superuser_required()
@method_decorator(login_required, name='dispatch')
class AnalysisUpdateView(UpdateView):
    model = AnalysisArticle
    fields = ('title','category','description','image' )
    template_name = 'edit_analysis.html'
    pk_url_kwarg = 'analysis_article_pk'
    context_object_name = 'analysis'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(starter=self.request.user)

    def form_valid(self, form):
        analysis = form.save(commit=False)
        analysis.updated_by = self.request.user
        analysis.updated_at = timezone.now()
        analysis.save()
        return redirect('analysis_posts', analysis_article_pk=analysis.pk)

@superuser_required()
class AnalysisDelete(DeleteView):
    model = AnalysisArticle
    success_url = reverse_lazy('analysis')


class AnalysisListView(ListView):
    model = AnalysisArticle
    context_object_name = 'analysis_list'
    template_name = 'analysis_and_opinion.html'
    paginate_by = 10
    class Meta:
        ordering = ['-last_updated']

def analysis_posts(request, analysis_article_pk):
    analysis_article = get_object_or_404(AnalysisArticle, pk=analysis_article_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.analysis_article = analysis_article
            post.created_by = request.user
            post.save()
    else:
        form = PostForm()
    return render(request, 'analysis_post.html', {'analysis_article' : analysis_article, 'form':form })


@login_required
def reply_analysis_article(request, analysis_article_pk):
    analysis_article = get_object_or_404(AnalysisArticle, pk=analysis_article_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.analysis_article = analysis_article
            post.created_by = request.user
            post.save()
            return redirect('analysis_posts', analysis_article_pk=analysis_article_pk)
    else:
        form = PostForm()
    return render(request, 'reply_analysis_article.html', {'analysis_article': analysis_article, 'form': form})


@method_decorator(login_required, name='dispatch')
class AnalysisPostUpdateView(UpdateView):
    model = AnalysisPost
    fields = ('message', )
    template_name = 'edit_analysis_post.html'
    pk_url_kwarg = 'analysis_post_pk'
    context_object_name = 'analysis_post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        analysis_post = form.save(commit=False)
        analysis_post.updated_by = self.request.user
        analysis_post.updated_at = timezone.now()
        analysis_post.save()
        return redirect('analysis_posts', analysis_article_pk=analysis_post.analysis_article.pk)


@login_required
def reply_analysis_post(request, analysis_article_pk, analysis_post_pk):
    analysis_post = get_object_or_404(AnalysisPost, pk=analysis_post_pk)
    if request.method == 'POST':
        form = AnalysisCommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.analysis_post = analysis_post
            post.created_by = request.user
            post.save()
            return redirect('analysis_posts', analysis_article_pk=analysis_article_pk)
    else:
        form = AnalysisCommentForm()
    return render(request, 'reply_analysis_post.html', {'analysis_post': analysis_post, 'form': form})


@login_required
def analysis_post_delete(request, analysis_article_pk, analysis_post_pk):
    analysis_post = get_object_or_404(AnalysisPost, pk=analysis_post_pk)
    creator = analysis_post.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        analysis_post.delete()
        return redirect('analysis_posts', analysis_article_pk=analysis_article_pk)
    
    context= {'analysis_post': analysis_post,
              'creator': creator,
              }


@method_decorator(login_required, name='dispatch')
class AnalysisCommentUpdateView(UpdateView):
    model = AnalysisComment
    fields = ('message', )
    template_name = 'edit_analysis_comment.html'
    pk_url_kwarg = 'analysis_comment_pk'
    context_object_name = 'analysis_comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        analysis_comment = form.save(commit=False)
        analysis_comment.updated_by = self.request.user
        analysis_comment.updated_at = timezone.now()
        analysis_comment.save()
        return redirect('analysis_posts', analysis_article_pk=analysis_comment.analysis_post.analysis_article.pk)


@login_required
def analysis_comment_delete(request, analysis_article_pk, analysis_post_pk, analysis_comment_pk):
    analysis_comment = get_object_or_404(AnalysisComment, pk=analysis_comment_pk)
    creator = analysis_comment.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        analysis_comment.delete()
        return redirect('analysis_posts', analysis_article_pk=analysis_article_pk)
    
    context= {'analysis_comment': analysis_comment,
              'creator': creator,
              }



@login_required
def reply_analysis_comment(request, analysis_article_pk, analysis_post_pk, analysis_comment_pk):
    analysis_comment = get_object_or_404(AnalysisComment, pk=analysis_comment_pk)
    if request.method == 'POST':
        form = AnalysisCommentForm2(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.analysis_comment = analysis_comment
            comment.created_by = request.user
            comment.save()
            return redirect('analysis_posts', analysis_article_pk=analysis_article_pk)
    else:
        form = AnalysisCommentForm2()
    return render(request, 'reply_analysis_comment.html', {'analysis_comment': analysis_comment, 'form': form})



@login_required
def analysis_comment2_delete(request, analysis_article_pk, analysis_post_pk, analysis_comment_pk, analysis_comment2_pk):
    analysis_comment2 = get_object_or_404(AnalysisComment2, pk=analysis_comment2_pk)
    creator = analysis_comment2.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        analysis_comment2.delete()
        return redirect('analysis_posts', analysis_article_pk=analysis_article_pk)
    
    context= {'analysis_comment2': analysis_comment2,
              'creator': creator,
              }

@method_decorator(login_required, name='dispatch')
class AnalysisComment2UpdateView(UpdateView):
    model = AnalysisComment2
    fields = ('message', )
    template_name = 'edit_analysis_comment2.html'
    pk_url_kwarg = 'analysis_comment2_pk'
    context_object_name = 'analysis_comment2'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        analysis_comment2 = form.save(commit=False)
        analysis_comment2.updated_by = self.request.user
        analysis_comment2.updated_at = timezone.now()
        analysis_comment2.save()
        return redirect('analysis_posts', analysis_article_pk=analysis_comment2.analysis_comment.analysis_post.analysis_article.pk)
