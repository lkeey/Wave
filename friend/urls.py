from django.urls import path

from friend.views import (
    send_friend_request,
    friend_requests,
    accept_friend_request,
    remove_friend,
    cancell_friend_request
)

urlpatterns = [
    # отправка
    path("friend_request", send_friend_request, name="friend_request"),
    # просмотр
    path("friend_requests/<user_id>/", friend_requests, name="friend_requests"),
    # подтверждение
    path("accept_friend_requests/<friend_request_id>/", accept_friend_request, name="accept_friend_requests"),
    # удаление
    path("friend_remove", remove_friend, name="remove_friend"),
    # отмена
    path("friend_request_decline/<friend_request_id>/", cancell_friend_request, name="decline_friend"),
]