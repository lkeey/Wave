from django.urls import path

from friend.views import (
    send_friend_request,
)

urlpatterns = [
    path("friend_request", send_friend_request, name="friend_request"),
]