from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse

from rest_framework.response import Response
from rest_framework import status
from rest_framework import decorators
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .forms import NewTopicForm, PostForm, CommentForm, Comment2Form

from analysis.models import AnalysisArticle
from SliderArticles.models import SliderArticle
from news.models import NewsArticle, NewsPost
from .models import Category, Topic, Post, Comment, Comment2, Preference
from .serializers import PreferenceSerializer, PostSerializer

class HomeListView(ListView):
    model = Post
    context_object_name = 'home_posts'
    template_name = 'index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the objects
        context['news_lists'] = NewsArticle.objects.order_by("-last_updated")
        context['topic_lists'] = Topic.objects.order_by("-last_updated")
        context['analysis_objects'] = AnalysisArticle.objects.order_by("-last_updated")
        return context
    class Meta:
            ordering = ['-id']

def not_found_404(request):
    return render(request, '404.html')    

def economic_calendar(request):
    analysis_objects = AnalysisArticle.objects.order_by("-last_updated")
    context = {'analysis_objects':analysis_objects}
    return render(request, 'economic-calendar.html', context)

def market_screener(request):
    analysis_objects = AnalysisArticle.objects.order_by("-last_updated")
    context = {'analysis_objects':analysis_objects}
    return render(request, 'market-screener.html', context)

def real_time_widget(request):
    analysis_objects = AnalysisArticle.objects.order_by("-last_updated")
    context = {'analysis_objects':analysis_objects}
    return render(request, 'real-time-widget.html', context)

class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'forum.html'

@method_decorator(login_required, name='dispatch')
class TopicUpdateView(UpdateView):
    model = Topic
    fields = ('subject', )
    template_name = 'edit_topic.html'
    pk_url_kwarg = 'topic_pk'
    context_object_name = 'topic'


    def form_valid(self, form):
        topic = form.save(commit=False)
        user = request.user.is_superuser.all()
        topic.updated_by = self.request.user
        topic.updated_at = timezone.now()
        topic.save()
        return redirect('category_topics', pk=topic.category.pk, topic_pk=topic.pk)


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'forum-topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['category'] = self.category
        return super().get_context_data(**kwargs)

    def get_context_data2(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['post_list'] = Post.objects.all()
        return context  

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        queryset = self.category.topics.order_by('-last_updated').annotate(replies=Count('posts'))
        return queryset

    class Meta:
            ordering = ['-last_updated']

# def category_topics(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     topics = category.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     return render(request, 'forum-topics.html', {'category': category, 'topics': topics})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic

        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        context['comments'] = Comment.objects.order_by('id')
        context['comments2'] = Comment2.objects.order_by('id')
        context['category_list'] = Category.objects.order_by('id')
        return context
        return super().get_context_data(**kwargs)

    class Meta:
            ordering = ['id']

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, category__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

    def post(self, request, pk, topic_pk, **kwargs):
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                topic = get_object_or_404(Topic, pk=topic_pk)
                post = form.save(commit=False)
                post.topic = topic
                post.created_by = request.user
                post.save()
        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.pk,
            page=topic.get_page_count()
        )
        return redirect(topic_post_url)

@login_required
def topic_delete(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    category = get_object_or_404(Category, pk=pk)
    creator = topic.starter.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        topic.delete()

        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
        topic_post_url = '{url}'.format(
            url=topic_url,
        )
        return redirect('category_topics', pk=pk)
    
    context= {'topic': topic,
              'creator': creator,
              }


@login_required
def post_delete(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    category = get_object_or_404(Category, pk=pk)
    creator = post.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        post.delete()

        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
        if '{url}?page={page}#{id}' == True:
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
        )
        else:
            topic_post_url = '{url}'.format(
                url=topic_url,
        )
        return redirect(topic_post_url)
    
    context= {'post': post,
              'creator': creator,
              }



@login_required
def comment_delete(request, pk, topic_pk, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = get_object_or_404(Post, pk=post_pk)
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    category = get_object_or_404(Category, pk=pk)
    creator = comment.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        comment.delete()

        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.pk,
            page=topic.get_page_count()
        )
        return redirect(topic_post_url)
    
    context= {'comment': comment,
              'creator': creator,
              }


@login_required
def comment2_delete(request, pk, topic_pk, post_pk, comment_pk, comment2_pk):
    comment2 = get_object_or_404(Comment2, pk=comment2_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = get_object_or_404(Post, pk=post_pk)
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    category = get_object_or_404(Category, pk=pk)
    creator = comment2.created_by.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        comment2.delete()

        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=post.pk,
            page=topic.get_page_count()
        )
        return redirect(topic_post_url)
    
    context= {'comment2': comment2,
              'creator': creator,
              }


# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def new_topic(request, pk):
    category = get_object_or_404(Category, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'category': category, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@login_required
def reply_post(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=post.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = CommentForm()
    return render(request, 'reply_post.html', {'post':post, 'form':form})


@login_required
def reply_comment(request, pk, topic_pk, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = Comment2Form(request.POST)
        if form.is_valid():
            comment2 = form.save(commit=False)
            comment2.comment = comment
            comment2.created_by = request.user
            comment2.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=comment.pk,
                page=comment.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = Comment2Form()
    return render(request, 'reply_comment.html', {'comment':comment, 'form':form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.category.pk, topic_pk=post.topic.pk)


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('message', )
    template_name = 'edit_comment.html'
    pk_url_kwarg = 'comment_pk'
    context_object_name = 'comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.updated_by = self.request.user
        comment.updated_at = timezone.now()
        comment.save()
        return redirect('topic_posts', pk=comment.post.topic.category.pk, topic_pk=comment.post.topic.pk)


@method_decorator(login_required, name='dispatch')
class Comment2UpdateView(UpdateView):
    model = Comment2
    fields = ('message', )
    template_name = 'edit_comment2.html'
    pk_url_kwarg = 'comment2_pk'
    context_object_name = 'comment2'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        comment2 = form.save(commit=False)
        comment2.updated_by = self.request.user
        comment2.updated_at = timezone.now()
        comment2.save()
        return redirect('topic_posts', pk=comment2.comment.post.topic.category.pk, topic_pk=comment2.comment.post.topic.pk)


@login_required
def postpreference(request, pk, topic_pk, post_pk, userpreference):
        
    if request.method == "POST":
            eachpost= get_object_or_404(Post, id=post_pk)
            obj=''
            valueobj=''
            try:
                obj= Preference.objects.get(user= request.user, post=eachpost)
                valueobj= obj.value #value of userpreference
                valueobj= int(valueobj)
                userpreference= int(userpreference)
        
                if valueobj != userpreference:

                        obj.delete()
                        upref= Preference()
                        upref.user= request.user
                        upref.post= eachpost
                        upref.value= userpreference

                        if userpreference == 1 and valueobj != 1:
                                eachpost.likes += 1
                                eachpost.dislikes -=1
                        elif userpreference == 2 and valueobj != 2:
                                eachpost.dislikes += 1
                                eachpost.likes -= 1
                        
                        upref.save()
                        eachpost.save()
                
                        context= {'eachpost': eachpost,
                          'post_pk': post_pk}

                        return render (request, 'topic_posts.html', context)

                elif valueobj == userpreference:
                        obj.delete()
                
                        if userpreference == 1:
                                eachpost.likes -= 1
                        elif userpreference == 2:
                                eachpost.dislikes -= 1

                        eachpost.save()

                        context= {'eachpost': eachpost,
                          'post_pk': post_pk}

                        return render (request, 'topic_posts.html', context)
                            
            except Preference.DoesNotExist:
                    upref= Preference()
                    upref.user= request.user
                    upref.post= eachpost
                    upref.value= userpreference
                    userpreference= int(userpreference)

                    if userpreference == 1:
                            eachpost.likes += 1
                    elif userpreference == 2:
                            eachpost.dislikes +=1

                    upref.save()
                    eachpost.save()                            
                    context= {'eachpost': eachpost,
                      'post_pk': post_pk}
                    return render (request, 'topic_posts.html', context)

    else:
        eachpost= get_object_or_404(Post, id=post_pk)
        context= {'eachpost': eachpost,
                  'post_pk': post_pk}
        return render (request, 'topic_posts.html', context)


@decorators.api_view(['POST', 'GET'])
@decorators.authentication_classes([SessionAuthentication])
def preference_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
        preferences = post.preference.all()
        resp = {
            'likes': preferences.filter(value=1).count(),
            'dislikes': preferences.filter(value=-1).count()
        }
        return Response(resp)

    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        preference = Preference.objects.get(post=post, user=request.user)
    except:
        preference=None

    ser = PreferenceSerializer(preference, data=request.data, 
        context={'request': request, 'post': post})
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    ser.save()
    preferences = post.preference.all()
    resp = {
        'likes': preferences.filter(value=1).count(),
        'dislikes': preferences.filter(value=-1).count()
    }
    return Response(resp)


class ListPosts(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
