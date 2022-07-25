
"""SocialWave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from .views import (
    PostDetailtView, 
    UserPostListView,
)    

from django.contrib.auth.decorators import login_required

from .models import (
    BookmarkPost,
    BookmarkComment
)

from . import views



urlpatterns = [
    # path('<str:username>/', UserPostsListView.as_view(), name='user_discussions_list'),   
    
    path('create', views.discussion_create, name='create_post'),   
    
    path('sign_up', views.sign_up, name='sign_up'),

    path('sign_in', views.sign_in, name='sign_in'),

    path('log_out', views.log_out, name='log_out'),

    path('settings', views.settings, name='settings'),
    
    path('<int:pk>/detail', PostDetailtView.as_view(), name='discussions_detail'),   

    path('like_post', views.like_post, name='like_post'),

    path('profile/<str:user_name>', views.profile_user, name='profile_user'),

    # path('comment/<post_id>', views.add_comment, name='add_comment'),

    # все посты
    path('', views.feed, name='posts_feed'),

    # profile
    # заменить класс на функцию
    path('<str:username>', UserPostListView.as_view(), name='user_posts_list'),   

    # path(r'^post/(?P<pk>\d+)/bookmark/$',
    #     login_required(views.BookmarkView.as_view(model=BookmarkPost)),
    #     name='post_bookmark'),
    
    path('post/<int:pk>/bookmark/',
        login_required(views.BookmarkView.as_view(model=BookmarkPost)),
        name='post_bookmark'),
    
    # path(r'api/^comment/(?P<pk>\d+)/bookmark/$',
    #     login_required(views.BookmarkView.as_view(model=BookmarkComment)),
    #     name='comment_bookmark'),
    
    path('comment/<int:pk>/bookmark/',
        login_required(views.BookmarkView.as_view(model=BookmarkComment)),
        name='comment_bookmark'),
    
]

