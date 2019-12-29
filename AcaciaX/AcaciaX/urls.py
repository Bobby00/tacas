"""AcaciaX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from news import views as news_views
from analysis import views as analysis_views
from accounts import views as accounts_views
from forum.views import CategoryListView, TopicListView, PostListView, HomeListView
from django.views.static import serve
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #WEB VIEWS URL PATTERNS
    path('', views.HomeListView.as_view(template_name='index.html'), name='home'),
    path('news/', news_views.news, name='news'),
    re_path(r'^news/(?P<news_article_pk>\d+)/$', news_views.news_posts, name='news_posts'),
    re_path(r'^news/(?P<news_article_pk>\d+)/reply/$', news_views.reply_news_article, name='reply_news_article'),

    path('analysis/', analysis_views.analysis, name='analysis'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/$', analysis_views.analysis_posts, name='analysis_posts'),
    re_path(r'^analysis/(?P<analysis_article_pk>\d+)/reply/$', analysis_views.reply_analysis_article, name='reply_analysis_article'),

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
    re_path(r'^forum/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
