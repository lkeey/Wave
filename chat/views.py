from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Chat, Message
from .forms import MessageForm
from django.db.models import Count

from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse

from django.views.generic import View


# Просмотр всех диалогов
class DialogsView(View):
    def get(self, request):
        print("USER-NAME", request.user, request.user.id)

        chats = Chat.objects.filter(members__in=[request.user.id])

        # print("UNREADED", Message.unreaded_objects.get_amount_unreaded().all().count())

        data = {
            'user': request.user, 
            'chats': chats,
# считаются сообщения, которые отправлены собеседником 
# (blog_tags.py - get_count_unreaded)
            'unreaded_dialogs': Message.unreaded_objects.get_amount_unreaded().all()
        }
        
        print("CONTEXT", chats)

        return render(request, 'chat/dialogs.html', data)

# Просмотр текущего диалога
class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                # все сообщения станут прочитанными, 
                # если сообщения отправлено другим пользователем

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
            print("CREATE MESSAGE", message)
            
            # if len(message.text) >= 1:
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        # return redirect(reverse('users:messages', kwargs={'chat_id': chat_id}))
        return redirect("messages", chat_id=chat_id)
        
# Создание диалога
class CreateDialogView(View):
    def get(self, request, user_id):

        # проверка - есть ли чат с такими пользователями
        # если он есть, то должно быть только два человека в нем
        # иначе диалог является чатом

        chats = Chat.objects.filter(
            members__in=[request.user.id, user_id], 
            type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        
        print("AMOUNT CHATS", chats)

        if chats.count() == 0:
            print("1st -", request.user.id)
            print("2nd -", user_id)

            chat = Chat.objects.create()
            chat.members.add(request.user.id)
            chat.members.add(user_id)
        
        else:
            print("SEARCH DIALOG")
            chat = chats.first()

        # return redirect(reverse('chat:messages', kwargs={'chat_id': chat.id}))
        return redirect("messages", chat_id=chat.id)