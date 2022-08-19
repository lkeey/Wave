from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User

from django.contrib import messages

import json

from friend.models import FriendList, FriendRequest
# Create your views here.

def friend_requests(request, *args, **kwargs):
    context = {}

    user = request.user

    user_id = kwargs.get("user_id")
    account = User.objects.get(pk=user_id)

    if account == user:
        friend_requests = FriendRequest.objects.filter(
            receiver=account, is_active=True
        )
        context["friend_requests"] = friend_requests

    else:
        return HttpResponse("NOT OWN SUBSRIBERS")

    return render(request, "friend/friend_requests.html", context)

def send_friend_request(request, *args, **kwargs):
    user = request.user 

    payload = {}


    if request.method == "POST":
        user_id = request.POST.get("receiver_user_id")

        # request.session['user_id'] = user_id

        if user_id:
            receiver = User.objects.get(pk=user_id)

            try:
                # Get any friend request (active and not-active)
            
                friend_requests = FriendRequest.objects.filter(
                    sender=user,
                    receiver=receiver
                )
                # find if any of them is active
                try:
                    for req in friend_requests:
                        if req.is_active:

                            messages.error(request, f'Friend Request Already Sent!')

                            raise Exception("You already sent them a friend request")
                
                    # if none are active, then create a new friend request
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['result'] = "success"
                    payload['response'] = "Friend Request Sent"
                    messages.success(request, f'Friend Request To {receiver} Successfully Sent!')

                    
                except Exception as _Ex:
                    payload['result'] = "error"
                    payload["response"] = str(_Ex)
                    messages.error(request, f'Error Occured!')

                
            except FriendRequest.DoesNotExist:
                # There are no friends, so create one
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['friend_request'] = "Friend Request Sent"
                messages.success(request, f'Friend Request To {receiver} Successfully Sent!')
            
            if payload["response"] == None:
                payload["response"] = "Something Wrong"
                messages.error(request, f'Error Occured!')
        else:
            payload["response"] = "Unable to send friend request"   
            messages.error(request, f'Error Occured!')

    return HttpResponse(    
        json.dumps(payload),
        content_type="application/json"
    )   

def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "GET":
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # receiver is user
            if friend_request.receiver == user:
                if friend_request:
                    # found the request
                    print(f"request - {friend_request.receiver} - {friend_request.sender}")
                    
                    # request.session['user_id'] = friend_request.sender

                    friend_request.accept()
                    payload["response"] = "Friend Request Accepted"
                    messages.info(request, f'Friend Request From {friend_request.sender} Was Accepted')

                else:
                    payload["response"] = "Something Wrong"
                    messages.error(request, f'Error Occured!')

            else:
                payload["response"] = "Thats not your request"
                messages.error(request, f'Error Occured!')

        else:
            payload["response"] = "Unable to accept"
            messages.error(request, f'Error Occured!')

    return HttpResponse(
        json.dumps(payload),
        content_type="application/json"
    )
        
def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "POST":
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            # request.session['user_id'] = user_id

# чтобы сделать подписчиков после удаления из друзей,
# нужно отправлять следующий запрос на дружбу:
#   receiver = request.user
#   sender = removee = receiver_user_id
#           + добавить в метод
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)

                payload["response"] = "Successfully removed"
                messages.warning(request, f'{removee} Was Removed From Your Friend List')

            except:
                payload["response"] = "Something wrong"
                messages.error(request, f'Error Occured!')

        else:
            payload["response"] = "Something wrong"
            messages.error(request, f'Error Occured!')

    return HttpResponse(
        json.dumps(payload),
        content_type="application/json"
    )


def cancell_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "GET":
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            
            # if friend_request.receiver == user:
            if friend_request:
                # request.session['user_id'] = friend_request.sender

                # found the request
                friend_request.cancel()
                payload['response'] = "Friend Request Cancelled"
                
                messages.warning(request, f'Friend Request For {friend_request.receiver} Was Cancelled')
            
            else:
                payload["response"] = "Smth went wrong"
                messages.error(request, f'Error Occured!')
            # else:
            #     payload["response"] = "Thats not your request"
        else:
            payload["response"] = "Unable to decline"
            messages.error(request, f'Error Occured!')

    return HttpResponse(
        json.dumps(payload),
        content_type="application/json"
    )

