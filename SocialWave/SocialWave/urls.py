
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('__debug__/', include('debug_toolbar.urls')),
    
    # https://www.youtube.com/watch?v=d1w1qL4aatY&list=PLuZJ9n46uMzXVj9JEjULImuBKRVKKS9To&index=11
    # path('register/', user_views.register, name='register'),
    # path('login/', user_views.register, name='register'),
    # path('logout/', user_views.register, name='register'),
    # path('password_reset/', user_views.register, name='register'),
    # path('password_reset/done/', user_views.register, name='register'),
    # path('register/', user_views.register, name='register'),
    # path('register/', user_views.register, name='register'),
    # path('register/', user_views.register, name='register'),
    
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT,
        )

if settings.DEBUG:
    import debug_toolbar

    # показывает toolbar
    urlpatterns = [
        path('__debug__/',
        include(debug_toolbar.urls)),
    ] + urlpatterns