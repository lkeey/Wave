from django.urls import path
from . import views

urlpatterns = [

    # path('', views.home, name='home'),
    # path('<str:room>/<str:name>/', views.room, name='room'),
    # path('checkview', views.checkview, name='checkview'),
    # path('send', views.send, name='send'),
    # path('getMessages/<str:room>', views.getMessages, name='getMessages'),

    path('', views.DialogsView.as_view(), name='home'),
    
    path('create/<user_id>', views.CreateDialogView.as_view(), name='create_conversation'),
    
    path('create_group', views.CreateGroupView.as_view(), name='create_group'),
    
    path('conversation/<int:chat_id>', views.MessagesView.as_view(), name='messages'),

    path('settings_group/<int:pk>', views.GroupSettings.as_view(), name='group_settings'),

]