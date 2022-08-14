from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User

import json

from friend.models import FriendRequest
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
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request")
                
                    # if none are active, then create a new friend request
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['result'] = "success"
                    payload['response'] = "Friend Request Sent"
                    
                except Exception as _Ex:
                    payload['result'] = "error"
                    payload["response"] = str(_Ex)

                
            except FriendRequest.DoesNotExist:
                # There are no friends, so create one
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['friend_request'] = "Friend Request Sent"

            if payload["response"] == None:
                payload["response"] = "Something Wrong"

        else:
            payload["response"] = "Unable to send friend request"   

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
                    friend_request.accept()
                    payload["response"] = "Friend Request Accepted"

                else:
                    payload["response"] = "Something Wrong"
            else:
                payload["response"] = "Thats not your request"
        else:
            payload["response"] = "Unable to accept"
    
    return HttpResponse(
        json.dumps(payload),
        content_type="application/json"
    )
        

        