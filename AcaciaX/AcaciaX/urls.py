from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve

from news import views as news_views
from analysis import views as analysis_views
from SliderArticles import views as article_views
from accounts import views as accounts_views
from forum.views import CategoryListView, TopicListView, PostListView, HomeListView
from django.views.static import serve
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #WEB VIEWS URL PATTERNS
    path('', views.HomeListView.as_view(template_name='index.html'), name='home'),
    path('404/', views.not_found_404, name='404'),

    #NEWS APP URL PATTERNS
    path('news/', news_views.NewsListView.as_view(), name='news'),
    re_path(r'^news/new/$', news_views.new_news_article, name='new_news'),
    re_path(r'^news/(?P<news_pk>\d+)/edit/$', news_views.NewsUpdateView.as_view(), name='edit_news'),
    re_path(r'^news/(?P<pk>\d+)/delete/$', news_views.NewsDelete.as_view(), name='delete_news'),
    re_path(r'^news/(?P<news_article_pk>\d+)/$', news_views.news_posts, name='news_posts'),
    re_path(r'^news/(?P<news_article_pk>\d+)/reply/$', news_views.reply_news_article, name='reply_news_article'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/delete/$', news_views.news_post_delete, name='delete_news_post'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/edit/$', news_views.NewsPostUpdateView.as_view(), name='edit_news_post'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/reply/$', news_views.reply_news_post, name='reply_news_post'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/comments/(?P<news_comment_pk>\d+)/edit/$', news_views.NewsCommentUpdateView.as_view(), name='edit_news_comment'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/comments/(?P<news_comment_pk>\d+)/reply/$', news_views.reply_news_comment, name='reply_news_comment'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/comments/(?P<news_comment_pk>\d+)/delete/$', news_views.news_comment_delete, name='delete_news_comment'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/comments/(?P<news_comment_pk>\d+)/comments2/(?P<news_comment2_pk>\d+)/edit/$', news_views.NewsComment2UpdateView.as_view(), name='edit_news_comment2'),
    re_path(r'^news/(?P<news_article_pk>\d+)/posts/(?P<news_post_pk>\d+)/comments/(?P<news_comment_pk>\d+)/comments2/(?P<news_comment2_pk>\d+)/delete/$', news_views.news_comment2_delete, name='delete_news_comment2'),


    # path('articles/', article_views.ArticleListView.as_view(), name='article'),
    # re_path(r'^articles/new/$', article_views.new_article, name='new_article'),
    # re_path(r'^articles/(?P<article_pk>\d+)/edit/$', article_views.ArticleUpdateView.as_view(), name='edit_article'),
    # re_path(r'^articles/(?P<pk>\d+)/delete/$', article_views.ArticleDelete.as_view(), name='delete_article'),
    # re_path(r'^articles/(?P<article_pk>\d+)/$', article_views.article_posts, name='article_posts'),
    # re_path(r'^articles/(?P<article_pk>\d+)/reply/$', article_views.reply_article, name='reply_article'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/edit/$', article_views.ArticlePostUpdateView.as_view(), name='edit_article_post'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/delete/$', article_views.article_post_delete, name='delete_article_post'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/reply/$', article_views.reply_article_post, name='reply_article_post'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/comments/(?P<article_comment_pk>\d+)/edit/$', article_views.ArticleCommentUpdateView.as_view(), name='edit_article_comment'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/comments/(?P<article_comment_pk>\d+)/reply/$', article_views.reply_article_comment, name='reply_article_comment'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/comments/(?P<article_comment_pk>\d+)/delete/$', article_views.article_comment_delete, name='delete_article_comment'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/comments/(?P<article_comment_pk>\d+)/comments2/(?P<article_comment2_pk>\d+)/edit/$', article_views.ArticleComment2UpdateView.as_view(), name='edit_article_comment2'),
    # re_path(r'^articles/(?P<article_pk>\d+)/posts/(?P<article_post_pk>\d+)/comments/(?P<article_comment_pk>\d+)/comments2/(?P<article_comment2_pk>\d+)/delete/$', article_views.article_comment2_delete, name='delete_article_comment2'),



    path('analysis/', analysis_views.AnalysisListView.as_view(), name='analysis'),
    re_path(r'^analysis/new/$', analysis_views.new_analysis, name='new_analysis'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/edit/$', analysis_views.AnalysisUpdateView.as_view(), name='edit_analysis'),
    re_path(r'^analysis/(?P<pk>\d+)/delete/$', analysis_views.AnalysisDelete.as_view(), name='delete_analysis'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/$', analysis_views.analysis_posts, name='analysis_posts'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/reply/$', analysis_views.reply_analysis_article, name='reply_analysis_article'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/edit/$', analysis_views.AnalysisPostUpdateView.as_view(), name='edit_analysis_post'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/delete/$', analysis_views.analysis_post_delete, name='delete_analysis_post'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/reply/$', analysis_views.reply_analysis_post, name='reply_analysis_post'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/comments/(?P<analysis_comment_pk>\d+)/edit/$', analysis_views.AnalysisCommentUpdateView.as_view(), name='edit_analysis_comment'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/comments/(?P<analysis_comment_pk>\d+)/delete/$', analysis_views.analysis_comment_delete, name='delete_analysis_comment'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/comments/(?P<analysis_comment_pk>\d+)/reply/$', analysis_views.reply_analysis_comment, name='reply_analysis_comment'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/comments/(?P<analysis_comment_pk>\d+)/comments2/(?P<analysis_comment2_pk>\d+)/edit/$', analysis_views.AnalysisComment2UpdateView.as_view(), name='edit_analysis_comment2'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/posts/(?P<analysis_post_pk>\d+)/comments/(?P<analysis_comment_pk>\d+)/comments2/(?P<analysis_comment2_pk>\d+)/delete/$', analysis_views.analysis_comment2_delete, name='delete_analysis_comment2'),


    path('economic_calendar/', views.economic_calendar, name='economic_calendar'),
    path('market_screener/', views.market_screener, name='market_screener'),
    path('real_time_widget/', views.real_time_widget, name='real_time_widget'),

    #ACCOUNTS URL PATTERNS
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),

    path('settings/account/profile_summary', accounts_views.ProfileSummaryView.as_view(), name='profile_summary'),
    path('settings/account/profile_notifications', accounts_views.ProfileNotificationView.as_view(), name='profile_notifications'),
    path('settings/account/profile_activity', accounts_views.ProfileActivityView.as_view(), name='profile_activity'),
    path('settings/account/profile_messages', accounts_views.ProfileMessageView.as_view(), name='profile_messages'),
    path('settings/account/profile_badges', accounts_views.ProfileBadgeView.as_view(), name='profile_badges'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),

    #ACCOUNT RECOVERY URLS
    re_path(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt' ), name='password_reset'),
    re_path(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    re_path(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    #FORUM URL PATTERNS
    path('forum/', CategoryListView.as_view(), name='forum'),
    re_path(r'^forum/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='category_topics'),
    re_path(r'^forum/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/edit/$', views.TopicUpdateView.as_view(), name='edit_topic'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/delete/$', views.topic_delete, name='delete_topic'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/reply/$', views.reply_post, name='reply_post'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/delete/$', views.post_delete, name='delete_post'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_post'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/edit/$', views.CommentUpdateView.as_view(), name='edit_comment'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/reply/$', views.reply_comment, name='reply_comment'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='delete_comment'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/comments2/(?P<comment2_pk>\d+)/edit/$', views.Comment2UpdateView.as_view(), name='edit_comment2'),
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/comments2/(?P<comment2_pk>\d+)/delete/$', views.comment2_delete, name='delete_comment2'),
    re_path(r'^api/forum/posts/(?P<post_id>\d+)/preference/$', views.preference_view), 
    re_path(r'^api/forum/posts/', views.ListPosts.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
