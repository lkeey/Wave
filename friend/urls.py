from django.urls import path

from friend.views import (
    send_friend_request,
    friend_requests,
    accept_friend_request,
)

urlpatterns = [
    # отправка
    path("friend_request", send_friend_request, name="friend_request"),
    # просмотр
    path("friend_requests/<user_id>/", friend_requests, name="friend_requests"),
    # подтверждение
    path("accept_friend_requests/<friend_request_id>/", accept_friend_request, name="accept_friend_requests"),
]