from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from .models import AnalysisArticle, AnalysisPost

from analysis.forms import PostForm

class AnalysisListView(ListView):
    model = AnalysisArticle
    context_object_name = 'analysis_list'
    template_name = 'analysis_and_opinion.html'
    paginate_by = 10


def analysis_posts(request, analysis_article_pk):
	analysis_article = get_object_or_404(AnalysisArticle, pk=analysis_article_pk)
	return render(request, 'analysis_post.html', {'analysis_article' : analysis_article})


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
