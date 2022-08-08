from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Chat, Message
from .forms import MessageForm
from django.db.models import Count

from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse

from django.views.generic import View


# Create your views here.

# def home(request):
#     # user enter name of group
#     return render(request, 'chat/home.html')

# def room(request, room, name):
#     # here users can change them messages

#     room_details = Room.objects.get(name=room)

#     data = {
#         'room': room,
#         'name': name,
#         'room_details': room_details,
#     }

#     return render(request, 'chat/room.html', data)

# def checkview(request):
#     # check if group is exist
#     # show button => click it => show room
#     room = request.POST['room_name']

#     if not(Room.objects.filter(name=room).exists()):
#         new_room = Room.objects.create(name=room)
#         new_room.save()

#     data = {
#         'room': room,
      
#     }

#     # if Room.objects.filter(name=room).exists():
#     #     return redirect('{% url "room" room=room %}')

#     # else:
#     #     new_room = Room.objects.create(name=room)
#     #     new_room.save()
#     #     return redirect('{% url "room" room=room %}')

#     return render(request, 'chat/loading.html', data)

# def send(request):
    
#     message = request.POST['message']
#     username = request.POST['username']
#     room_id = request.POST['room_id']

#     new_message = Message.objects.create(value=message, 
#                                 user=username, 
#                                 room=room_id
#                                 )
#     new_message.save()

#     return HttpResponse('Message sent successfully')

# def getMessages(request, room):

#     room_details = Room.objects.get(name=room)

#     messages = Message.objects.filter(room=room_details.id)

#     return JsonResponse({"messages":list(messages.values())})

# Просмотр всех диалогов
class DialogsView(View):
    def get(self, request):
        print("USER-NAME", request.user, request.user.id)

        chats = Chat.objects.filter(members__in=[request.user.id])
        
        data = {
            'user_profile': request.user, 
            'chats': chats
        }
        
        print("CONTEXT", chats)

        return render(request, 'chat/dialogs.html', data)

# Просмотр текущего диалога
class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(readable=False).exclude(author=request.user).update(readable=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        context = {
                'user': request.user,
                'chat': chat,
                'form': MessageForm()
            }

        return render(request,'chat/messages.html', context)
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        # return redirect(reverse('users:messages', kwargs={'chat_id': chat_id}))
        return redirect("messages", chat_id=chat_id)
        
# Создание диалога
class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.type).annotate(c=Count('members')).filter(c=2)
        
        if chats.count() == 0:
            print("1st -", request.user.id)
            print("2nd -", user_id)

            chat = Chat.objects.create()
            chat.members.add(request.user.id)
            chat.members.add(user_id)
        
        else:
            chat = chats.first()

        # return redirect(reverse('chat:messages', kwargs={'chat_id': chat.id}))
        return redirect("messages", chat_id=chat.id)