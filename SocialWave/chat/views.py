from email import message
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

# Create your views here.

def home(request):
    # user enter name of group
    return render(request, 'chat/home.html')

def room(request, room, name):
    # here users can change them messages

    room_details = Room.objects.get(name=room)

    data = {
        'room': room,
        'name': name,
        'room_details': room_details,
    }


    return render(request, 'chat/room.html', data)

def checkview(request):
    # check if group is exist
    # show button => click it => show room
    room = request.POST['room_name']

    if not(Room.objects.filter(name=room).exists()):
        new_room = Room.objects.create(name=room)
        new_room.save()

    data = {
        'room': room,
      
    }

    # if Room.objects.filter(name=room).exists():
    #     return redirect('{% url "room" room=room %}')

    # else:
    #     new_room = Room.objects.create(name=room)
    #     new_room.save()
    #     return redirect('{% url "room" room=room %}')

    return render(request, 'chat/loading.html', data)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()

    return HttpResponse('Message sent successfully')

def getMessages(request, room):

    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)

    return JsonResponse({"messages":list(messages.values())})