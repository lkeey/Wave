from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User

import json

from friend.models import FriendRequest
# Create your views here.


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
