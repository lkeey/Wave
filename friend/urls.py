from django.urls import path

from friend.views import (
    send_friend_request,
    friend_requests
)

urlpatterns = [
    path("friend_request", send_friend_request, name="friend_request"),
    path("friend_requests/<user_id>/", friend_requests, name="friend_requests"),
]