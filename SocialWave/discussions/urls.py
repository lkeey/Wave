
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
from discussions.views import DiscussionDetailtView, UserDiscussionListView
from . import views

urlpatterns = [

    path('<str:username>/', UserDiscussionListView.as_view(), name='user_discussions_list'),   
    
    path('create', views.discussion_create, name='create_post'),   
    
    path('<int:pk>/detail', DiscussionDetailtView.as_view(), name='discussions_detail'),   
]

