from django import template
from django import template
from blog.models import CommentLike, PostLike
from chat.models import Message, Chat
from blog.models import User
from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from django.core import serializers
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
        user = User.objects.get(username=user)

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

@register.simple_tag
def get_user(username):
    print("user-get", username)
    try:
        user = User.objects.get(username=username)

    except:
        user = User.objects.get(user=username)
    
    return user
# for (var i in response["users_data"]) {
#                     var current = response["users_data"][i]['username']
#                     alert(current);
#                     var user = "{% get_user current %}";
#                     alert(user);
#                     html += user;
#                 }; 
# const user_input = $("#user-input")
    # const search_icon = $('#search-icon')
    # const artists_div = $('#replaceable-content')
    # const endpoint = '{% url "all_users" %}'
    # const delay_by_in_ms = 700
    # let scheduled_function = false

    # let ajax_call = function (endpoint, request_parameters) {
    #     $.getJSON(endpoint, request_parameters)
    #         .done(response => {
    #             response = JSON.parse(response)
    #             alert(response)
    #             // fade out the artists_div, then:
    #             artists_div.fadeTo('slow', 0).promise().then(() => {
    #             // replace the HTML contents

    #             var html = "";
    #             var users = response['users_data'];

    #             users = "{% get_user users %}";
    #             alert(users)
    #             users = JSON.parse(users);
    #             alert(users)
                
    #             for (var i in users) {
    #                 alert(users[i])
    #             }

    #             artists_div.html(html);
    #             // fade-in the div with new contents
    #             artists_div.fadeTo('slow', 1)
    #             // stop animating search icon
    #             search_icon.removeClass('blink')

    #             })
    #         })
    # }


    # user_input.on('keyup', function () {

    #     const request_parameters = {
    #         q: $(this).val() // value of user_input: the HTML element with ID user-input
    #     }

    #     // start animating the search icon with the CSS class
    #     search_icon.addClass('blink')

    #     // if scheduled_function is NOT false, cancel the execution of the function
    #     if (scheduled_function) {
    #         clearTimeout(scheduled_function)
    #     }

    #     // setTimeout returns the ID of the function to be executed
    #     scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
    # })

# response.forEach( function (item) {
                        # var currentUser = item.username
                    #     alert(currentUser)

                    #     currentUser = "{% get_user currentUser %}"
                        
                    #     html += `Hi, ${currentUser}`
                    # })