from email import message
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib import messages

from .models import Chat, Group, Message, User
from .forms import MessageForm, GroupEditForm
from django.db.models import Count

# from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse

from django.views.generic import View

from django.db.models import Q


# Просмотр всех диалогов
class DialogsView(View):
    def get(self, request):
        print("USER-NAME", request.user, request.user.id)

        chats = Chat.objects.filter(members__in=[request.user.id])

        count = Message.unreaded_objects.get_amount_unreaded().all().filter(chat__members__in=[request.user.id]).exclude(author=request.user)

        # print("UNREADED", Message.unreaded_objects.get_amount_unreaded().all().count())

        data = {
            'user': request.user, 
            'chats': chats,
            # 'count': count,
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
                first_message_unread = Message.unreaded_objects.get_amount_unreaded().exclude(author=request.user).filter(chat=chat).first()
                
                if not first_message_unread:
                    first_message_unread = Message.unreaded_objects.get_earliest_message()
                
                print("first_message_unread",first_message_unread)
                
                chat.message_set.filter(readable=False).exclude(author=request.user).update(readable=True)
            
            else:
                chat = None

        except Chat.DoesNotExist:
            chat = None


        context = {
                'user': request.user,
                'chat': chat,
                'form': MessageForm(),
                'unread_1st': first_message_unread
            }

        return render(request,'chat/messages.html', context)
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            if str(message).isspace() or len(str(message)) == 0:
                print("NOOO!!!")

            else:
                print("CREATE MESSAGE", message)
                print(len(str(message)))

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

            if int(request.user.id) == int(user_id):
                user = get_object_or_404(User, id=user_id
                )
                messages.error(request, 'Access denied')
                return redirect('profile_user', user_name=user.username) 
   
            else:
                print(request.user.id == user_id)
                chat = Chat.objects.create()
                chat.members.add(request.user.id)
                chat.members.add(user_id)
        else:
            print("SEARCH DIALOG")
            chat = chats.first()

        # return redirect(reverse('chat:messages', kwargs={'chat_id': chat.id}))
        return redirect("messages", chat_id=chat.id)

# создание группы
class CreateGroupView(View):
    form_class = GroupEditForm

    def get(self, request):
        group = Chat.objects.create()
        group.members.add(request.user.id)

        context = {
            'user': request.user,
            'group': group,
            'form': GroupEditForm(),
        }

        return render(request,'chat/group_settings.html', context)

    def post(self, request, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form, request)

        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        form = GroupEditForm(data=request.POST)
        # group_id = request.FILES.get('image')
        # print("img", group_id)

        group_id = request.POST['group_id']
        print("id", group_id)

        if form.is_valid() and group_id:
            group = Group.get_object_or_404(id=group_id)

            data = form.save(commit=False)

            print("data", data)
        
        return redirect("home")
