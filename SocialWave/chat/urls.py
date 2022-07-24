from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('<str:room>/<str:name>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>', views.getMessages, name='getMessages'),

    # path(r'^dialogs/$', views.DialogsView.as_view(), name='dialogs'),
    # path(r'^dialogs/create/(?P<user_id>\d+)/$', views.CreateDialogView.as_view(), name='create_dialog'),
    # path(r'^dialogs/(?P<chat_id>\d+)/$', views.MessagesView.as_view(), name='messages'),

]