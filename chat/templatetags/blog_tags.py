from django import template
from django import template
from blog.models import CommentLike, PostLike
from chat.models import Message, Chat

from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus

from django.db.models import Q
from django.shortcuts import get_object_or_404

register = template.Library()

@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None

@register.simple_tag
def myDate(value):
    #arg is optional and not needed but you could supply your own formatting if you want.
    # dateformatted = value.strftime("%b %d, %Y at %I:%M %p")
    dateformatted = value.strftime("%I:%M %p")
    return dateformatted

@register.simple_tag
def get_count_unreaded(chat, participant):
    count = Message.unreaded_objects.get_amount_unreaded().all().filter(chat=chat, author=participant).count()
    # names = Message.unreaded_objects.all().filter(chat=chat.id)
    
    return count

@register.simple_tag
def get_all_unreaded(user):

    count = Message.unreaded_objects.get_amount_unreaded().all().filter(chat__members__in=[user.id]).exclude(author=user).count()

    return count

@register.simple_tag
def was_liked(user, id):

    try:
        PostLike.objects.get(user=user, obj_id=id)
        return True
    except PostLike.DoesNotExist:
        return False

@register.simple_tag
def was_liked_comm(user, id):

    try:
        CommentLike.objects.get(user=user, obj_id=id)
        return True
    except CommentLike.DoesNotExist:
        return False

@register.simple_tag
def get_user_data(account, user):
    # BASE VARIABLES
    is_self = True
    is_friend = False
    request_sent = None
    pending_friend_request_id = None

    # получение друзей аккаунта
    try:
        friend_list = FriendList.objects.get(user=account)
    except FriendList.DoesNotExist: 
        friend_list = FriendList(user=account)
        friend_list.save()

    friends = friend_list.friends.all()

    if user != account:
        is_self = False

        if friends.filter(pk=user.id):
                
                # есть в друзьях
                is_friend = True

        else:
            is_friend = False
            # CASES

            if get_friend_request_or_false(sender=account, receiver=user) != False:
                pending_friend_request_id = get_friend_request_or_false(
                    sender=account, receiver=user
                ).id

                # Запрос отправлен от кого-то мне(пользователю)
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                

            elif get_friend_request_or_false(sender=user, receiver=account) != False:
                # Я(пользователь) отправил кому-то запрос
                pending_friend_request_id = get_friend_request_or_false(
                    sender=user, receiver=account
                ).id

                
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value

            else:
                print("NONE")
                # Запрос НИКЕМ не был отправлен
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

    return {
        "is_self": is_self,
        "is_friend": is_friend,
        "request_sent": request_sent,
        "pending_friend_request_id": pending_friend_request_id,
    }
