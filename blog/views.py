from re import search

from django.conf import settings as project_settings

from django.contrib.sessions.models import Session
from django.utils import timezone
# for telegram
from django_telegram_login.widgets.constants import (
    SMALL, 
    MEDIUM, 
    LARGE,
    DISABLE_USER_PHOTO,
)

from PIL import Image

import numpy as np 

import qrcode

from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)
from django_telegram_login.authentication import verify_telegram_authentication

from django_telegram_login.errors import (
    NotTelegramDataError, 
    TelegramDataIsOutdatedError,
)


from django.http.response import HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist

from django.urls.base import reverse_lazy

from django.views.generic import (
    ListView, CreateView, 
    DetailView, View,
)
from django.views.generic.edit import FormMixin

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User, auth

from django.contrib.auth.mixins import LoginRequiredMixin
# https://docs.djandefgoproject.com/en/4.0/ref/contrib/
# messages/

from django.http import HttpResponse, HttpResponseNotAllowed

from django.contrib import messages

from django.views.generic.dates import timezone_today

from friend.models import FriendList, FriendRequest

from .models import (
    NotificationComment, NotificationCommentCreated, NotificationLike, Post, Profile, 
    PostLike, CommentLike,
    BookmarkComment, BookmarkPost,
)

from .forms import PostCreateForm, CommentForm

from django.contrib.auth.decorators import login_required

import json

from friend.utils import get_friend_request_or_false

from friend.friend_request_status import FriendRequestStatus

bot_name = project_settings.TELEGRAM_BOT_NAME
bot_token = project_settings.TELEGRAM_BOT_TOKEN
redirect_url = project_settings.TELEGRAM_LOGIN_REDIRECT_URL
name_site = 'http://127.0.0.1:8000/'

# Create your views here.

# class UserPostsListView(ListView):
#     # Модель пост в models.py
#     model = Post

#     # Имя шаблона html
#     template_name = 'discussions/user_discussions.html'

#     def get_context_data(self, **kwargs):

#         user = get_object_or_404(User,
#             username = self.kwargs.get('username')
#             )

#         queryset = Post.objects.filter(author=user)

#         context = super().get_context_data(**kwargs)

#         context['discussions post_user_list'] = queryset.order_by('-date_created')
        
#         return context

@login_required(login_url='sign_in')
def show_all_users(request):
    user = auth.get_user(request)

    users = User.objects.all()

    data = {}

    try:
        friend_list = FriendList.objects.get(user=user)
        print("friend_list", friend_list)
    except FriendList.DoesNotExist: 
        friend_list = FriendList(user=user)
        friend_list.save()

    friends = friend_list.friends.all()     

    if request.method == "GET":
        search_query = request.GET.get("search")
        if search_query:
            if len(search_query) > 0:
                search_results = users.filter(
                    username_icontains=search_query
                     ).distinct()

    data = {
        'user_global': user,
        'users': users,
        'friends': friends,
        # 'search_results': search_results,
    }

    return render(request, 'discussions/catalog_users.html', data)


def profiles_search_view(request, *args, **kwargs):
    context = {} 

    return render 

class PostDetailtView(FormMixin, DetailView):
    model = Post

    template_name = 'discussions/discussion_detail.html'
    context_object_name = 'discussion_detail'

    form_class = CommentForm

    # def get_pk(self):

    def get_success_url(self, **kwargs):
        return reverse_lazy('discussions_detail', kwargs={"pk":self.get_object().id})
    
   
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form, request)

        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        user_profile = Profile.objects.get(user=request.user)
        post = self.get_object()

        self.object = form.save(commit=False)
        self.object.post = post
        self.object.author = self.request.user

        post.amount_of_comments += 1
        post.save()

        self.object.save()

        # создание уведомления о создании комментария

        # проверка на существование уведомления
        notification, created_notificate = NotificationCommentCreated.objects.get_or_create(
            user=post.author,
            creator=request.user, obj_id=self.object.id
        )

        if not created_notificate:
            print("DELETED NOTIFICATION COMM")
            notification.delete()

        print("NOTITFICATION COMM", notification, notification.creator)

        return super().form_valid(form)

    # def get_context_data(self, **kwargs):

    #     user = get_object_or_404(User,
    #         username = self.kwargs.get('username')
    #         )

    #     user_profile = Profile.objects.get(user=user)

    #     context = super().get_context_data(**kwargs)

    #     context['user_profile'] = user_profile
        
    #     return context


@login_required(login_url='sign_in')
def discussion_create(request):
    print("USER", request.user)

    # если запрос POST. то тогда обрабатываем форму
    if request.method == 'POST':
        # Создадим экземпляр формы и заполним его данными запроса

        # Создадим форму для редактирования

        form = PostCreateForm(request.POST, request.FILES)
        print("FORM",form) 
        # данные пост для заполнения формы

        if form.is_valid():

            new_disccusion = form.save(commit=False)

            new_disccusion.author = request.user

            new_disccusion.image = request.FILES.get("image_upload")

            new_disccusion.save()

            # return redirect(new_disccusion.get_absolute_url())
            data = {
                "discussion_detail": new_disccusion,
                "form": CommentForm,
            }

            messages.info(request, 'The post was created successfully')
            messages.success(request, 'Now all SocialWave users will see it')

            return redirect('discussions_detail', pk=new_disccusion.pk)
            # return render(request, 'discussions/discussion_detail.html', data)

    
    # если get-запрос, то вернуть пустую форму
    formset = PostCreateForm()

    return render(request, 'discussions/create.html', {'formset': formset})

# for profile
class UserPostListView(ListView):
    # model in models.py
    model = Post

    # name of template
    template_name = 'discussions/profile.html'

    # save data # for cycle "for" in user_posts.html
    context_object_name = 'blog_post_user_list'

    # def get_queryset(self):
    #     user = get_object_or_404(
    #         User,
    #         username = self.kwargs.get('username'),
    #     )
    #     return Post.objects.filter(author=user).order_by('-date_created')

    # возвращает все посты
    # переопределяет стандартную функцию
    def get_context_data(self, **kwargs):
        # user = get_object_or_404(
        #     User, 
        #     username=self.kwargs.get('username')
        # )

        user = auth.get_user(self.request)

        user_profile = Profile.objects.get(user=user)

        queryset_posts = Post.objects.filter(author=user).order_by('-date_created')
        print("LEN", len(queryset_posts))

        query_posts_likes = PostLike.objects.filter(user=user).order_by('-obj')

        query_comm_likes = CommentLike.objects.filter(user=user).order_by('-obj')

        query_posts_favourite = BookmarkPost.objects.filter(user=user).order_by('-obj')

        friend_requests = None
        friend_list = None

        try:
            friend_list = FriendList.objects.get(user=user)

        except FriendList.DoesNotExist: 
            friend_list = FriendList(user=user)
            friend_list.save()

        friends = friend_list.friends.all()

        try:
            friend_requests = FriendRequest.objects.filter(
                receiver=user,
                is_active=True)
        except:
            pass

        # query_comm_favourite = BookmarkComment.objects.filter(user=user).order_by('-obj')

        # context = super().get_context_data(**kwargs)['blog_post_user_list'] = queryset
        context = {
            'user': user,

            'blog_post_user_list': queryset_posts,

            'like_post_user_list': query_posts_likes,
            'like_comm_user_list': query_comm_likes,

            'favourite_post_user_list': query_posts_favourite,
            # 'favourite_comm_user_list': query_comm_favourite,

            'user_profile': user_profile,

            'friend_requests': friend_requests,
            'friends': friends,

            "form": CommentForm,
        }
        return context

    def post(self, request, **kwargs):

        user_profile = Profile.objects.get(user=request.user)

        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            # bio = request.POST['bio']
            # location = request.POST['location']

            # user_profile.profile_img = image
            # user_profile.bio = bio
            # user_profile.location = location
            # user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('user_posts_list')

# все посты
@login_required(login_url='sign_in')
def feed(request):
    
    user = auth.get_user(request)

    friend_requests = FriendRequest.objects.filter(
            receiver=user.id, is_active=True
        )

    print("FRIEN_R", friend_requests)

    data = {
        "user": user,
        "all_posts": Post.objects.order_by('-date_created'),
        "form": CommentForm,
        "friend_requests_count": friend_requests.count(),
    }

    return render(request, 'discussions/posts_feed.html', data)

# registration
def sign_up(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        # email = request.POST['email']
        # telegram_id - default (0)
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if len(username) >= 3 and len(password) >= 8:


                # if User.objects.filter(email=email).exists():
                #     messages.info(request, "EMAIL WAS TAKEN")
                #     return redirect('sign_up')

                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username was taken")

                else:
                    # QR-code-img    
                    try:
                        filename = project_settings.MEDIA_ROOT + f"/qr-images/qr-{username}.png"

                        print("QR", filename)

                        # создать экземпляр объекта QRCode
                        qr = qrcode.QRCode(version=1, box_size=7, border=4)

                        # добавить данные в QR-код
                        qr.add_data(f"{name_site}profile/{username}")

                        # компилируем данные в массив QR-кода
                        qr.make()

                        # распечатать форму изображения
                        print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
                        
                        # переносим массив в реальное изображение
                        img = qr.make_image(fill_color="#eca1a6", back_color="black")
                        print("SAVE")
                
                        # сохраняем в файл
                        img.save(filename) 
                        print("SAVE")

                        # print("1",  self.qr_image)
                        # print("2",  self.qr_image.path)
                        # self.qr_image.path = self.qr_image.path.replace("blank-profile-img", f"qr-{self.user.username}")
                        # print("SELF_QR_IMAGE", self.qr_image)

                    except Exception as _ex:
                        print("Exception", _ex)

                    # create User
                    user = User.objects.create_user(
                        username=username,
                        # email=email,
                        password=password
                    )

                    user.save()

                    # redirect to settings
                    user_login = auth.authenticate(username=username, password=password)

                    auth.login(request, user_login)

                    # Create User's profile
                    user_model = User.objects.get(username=username)
                    
                    new_profile = Profile.objects.create(
                        user=user_model, 
                        id_user=user_model.id,
                        qr_image=f"qr-images/qr-{username}.png"                            
                    )

                    new_profile.save()

                    messages.info(request, f'Hello, {user.username}')
                    messages.success(request, 'We are glad to see you in SocialWave')

                    data = {
                            "all_posts": Post.objects.order_by('-date_created'),
                            "form": CommentForm,
                        }

                    # return render(request, 'discussions/posts_feed.html', data)
                    return redirect('posts_feed')
            else:
                messages.info(request, 'The username must be more than 2 characters and the password more than 7')


        else:
            messages.info(request, 'Password is not matching')
            return redirect('sign_up')


    return render(request, 'discussions/sign_up.html')

# logging
def sign_in(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            messages.info(request, f'Hello, {user.username}')
            messages.success(request, 'We are glad to see you in SocialWave')

            data = {
                    "all_posts": Post.objects.order_by('-date_created'),
                    "form": CommentForm,
                }

            # return render(request, 'discussions/posts_feed.html', data)
            return redirect('posts_feed')
        else:
            messages.warning(request, 'Data is invalid')

        
    telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {'telegram_login_widget': telegram_login_widget}

    return render(request, "discussions/sign_in.html", context)


# logging out
@login_required(login_url='sign_in')
def log_out(request):
    auth.logout(request)

    return redirect('sign_in')

# user's seettings
def settings(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            # bio = request.POST['bio']
            # location = request.POST['location']

            # user_profile.profile_img = image
            # user_profile.bio = bio
            # user_profile.location = location
            # user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')

    data = {
        'user_profile': user_profile
    }

    return render(request, 'discussions/settings.html', data)

# @login_required(login_url='sign_in') 
# def like_post(request):
#     username = request.user.username
#     post_id = request.GET.get('post_id')

#     post = Post.objects.get(id=post_id)

#     like_filter = LikePost.objects.filter(
#         post_id=post_id,
#         username=username
#     ).first()

#     if like_filter == None:
#         new_like = LikePost.objects.create(
#             post_id=post_id,
#             username=username
#         )

#         new_like.save()

#         post.amount_of_likes += 1
#         post.save()

#         return redirect('posts_feed')

#     else:
#         like_filter.delete()
#         post.amount_of_likes -= 1
#         post.save()
#         return redirect('posts_feed')

@login_required(login_url='sign_in')
def profile_user(request, user_name):
    user_global = request.user

    user = get_object_or_404(
            User, 
            username=user_name
        )

    user_profile = Profile.objects.get(user=user)

    user_posts = Post.objects.filter(author=user).order_by('-date_created')

    user_posts_length = len(user_posts)

    # Friend Requests

    try:
        friend_list = FriendList.objects.get(user=user)
        print("friend_list", friend_list)
    except FriendList.DoesNotExist: 
        friend_list = FriendList(user=user)
        friend_list.save()


    friends = friend_list.friends.all()

    print("FRIENDS", friends)


    # BASE VARIABLES
    is_self = True
    is_friend = False
    pending_friend_request_id = None
    friend_requests = None
    request_sent = None

    if user != user_global:
        # не является собой
        is_self = False

        if friends.filter(pk=user_global.id):
            
            # есть в друзьях
            is_friend = True

        else:
            print("HERE2")
            is_friend = False
            # CASES

            if get_friend_request_or_false(sender=user, receiver=user_global) != False:
                print("THEM")
                # Запрос отправлен от кого-то мне(пользователю)
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                
                pending_friend_request_id = get_friend_request_or_false(
                    sender=user, receiver=user_global
                ).id

            elif get_friend_request_or_false(sender=user_global, receiver=user) != False:
                # Я(пользователь) отправил кому-то запрос
                pending_friend_request_id = get_friend_request_or_false(
                    sender=user_global, receiver=user
                ).id

                print("YOU")
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value

            else:
                print("NONE")
                # Запрос НИКЕМ не был отправлен
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

    else:
        print("WARNING")
        # написать сообщение в шаблоне 
        try:
            friend_requests = FriendRequest.objects.filter(
                receiver=user_global,
                is_active=True)
            print("friend_requests",friend_requests)
        except:
            pass
     

    context = {
        'user_object': user,

        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,

        'is_self': is_self,
        'is_friend': is_friend,

        'friends': friends,
        'request': request,

        'request_sent': request_sent,
        'friend_requests': friend_requests,

        'pending_friend_request_id': pending_friend_request_id,

        "form": CommentForm,
    }

    return render(request, 'discussions/profile_user.html', context)

@login_required(login_url='sign_in')
def notifications_user(request):
    # user = get_object_or_404(
    #         User, 
    #         username=user_name
    #     )
    user = auth.get_user(request)
    # all_notifications = NotificationLike.objects.get(user=user_name)
    
    # queryset всех лайков
    queryset_likes_read = NotificationLike.objects.filter(user=user, readable=True)
    queryset_likes_unread = NotificationLike.objects.filter(user=user, readable=False)

    # queryset всех коммов
    queryset_comms_read = NotificationComment.objects.filter(user=user, readable=True)
    queryset_comms_unread = NotificationComment.objects.filter(user=user, readable=False)
   

    queryset_comms_created_read = NotificationCommentCreated.objects.filter(user=user, readable=True)
    queryset_comms_created_unread = NotificationCommentCreated.objects.filter(user=user, readable=False)
    
    # полный queryset
    # queryset_all_read = queryset_likes_read.union(queryset_comms_read)
    # queryset_all_unread = queryset_likes_unread.union(queryset_comms_unread)

    print("queryset_likes_read", queryset_likes_read)
    print("queryset_likes_unread", queryset_likes_unread)

    print("queryset_comms_read", queryset_comms_read)
    print("queryset_comms_unread", queryset_comms_unread)

    print("queryset_comms_created_read", queryset_comms_created_read)
    print("queryset_comms_created_unread", queryset_comms_created_unread)

    # print("all_notifications_read", queryset_all_read)
    # print("all_notifications_unread", queryset_all_unread)

    # queryset_all_read = queryset_all.filter(readable=True)
    # queryset_all_unread = queryset_all.filter(readable=False)

    all_notifications = (
        queryset_likes_read.count() + queryset_likes_unread.count() + 
        queryset_comms_read.count() + queryset_comms_unread.count() +
        queryset_comms_created_read.count() + queryset_comms_created_unread.count()
    )
    
    context = {
        'user_object': user,

        'queryset_likes_read': queryset_likes_read,
        'queryset_likes_unread': queryset_likes_unread,

        'queryset_comms_read': queryset_comms_read,
        'queryset_comms_unread': queryset_comms_unread,

        'queryset_comms_created_read': queryset_comms_created_read,
        'queryset_comms_created_unread': queryset_comms_created_unread,

        'all_notifications': all_notifications,

        # 'all_notifications_read': queryset_all_read,
        # 'all_notifications_unread': queryset_all_unread,
    
    }

    return render(request, 'discussions/notifications.html', context)

def success_notifications(request):
    user = auth.get_user(request)
    # Все уведомления были прочтены
    
    # queryset всех лайков на посты
    NotificationLike.objects.filter(user=user).update(readable=True)
    
    # queryset всех лайков на коммы
    NotificationComment.objects.filter(user=user).update(readable=True)
   
    # queryset всех коммов на пост
    NotificationCommentCreated.objects.filter(user=user).update(readable=True)
    
    # for notification in queryset_likes:
    #     if not notification.readable:
    #         # print("CHANGE ON TRUE", notification.obj)
    #         notification.readable = True
    #         notification.save()

    # for notification in queryset_comms:
    #     if not notification.readable:
    #         # print("CHANGE ON TRUE", notification.obj)
    #         notification.readable = True
    #         notification.save()

    
    return redirect('posts_feed')

# @login_required
# def add_comment(request, post_id):
#     if request.method == "POST":

#         form = CommentForm(request.POST)
#         post = get_object_or_404(Post, id=post_id)
    
#         if form.is_valid():
#             comment = Comment()
#             comment.path = []
#             comment.post_id = post
#             comment.author_id = auth.get_user(request)
#             comment.content = form.cleaned_data['comment_area']
#             comment.save()
    
#             # Django не позволяет увидеть ID комментария по мы не сохраним его, 
#             # хотя PostgreSQL имеет такие средства в своём арсенале, но пока не будем
#             # работать с сырыми SQL запросами, поэтому сформируем path после первого сохранения
#             # и пересохраним комментарий 
#             try:
#                 comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
#                 comment.path.append(comment.id)
            
#             except ObjectDoesNotExist:
#                 comment.path.append(comment.id)
    
#             comment.save()
    
#         return redirect(post.get_absolute_url())

# class EArticleView(View):
#     template_name = 'knowledge/article.html'
#     comment_form = CommentForm

#     def get(self, request,  *args, **kwargs):
#         post = get_object_or_404(Post, id=self.kwargs['post_id'])
#         context = {}
#         context.update(csrf(request))
#         user = auth.get_user(request)
#         context['post'] = post
#         # Помещаем в контекст все комментарии, которые относятся к статье
#         # попутно сортируя их по пути, ID автоинкрементируемые, поэтому
#         # проблем с иерархией комментариев не должно возникать
#         context['comments'] = post.comment_set.all().order_by('path')
#         context['next'] = post.get_absolute_url()
#         # Будем добавлять форму только в том случае, если пользователь авторизован
#         if user.is_authenticated:
#             context['form'] = self.comment_form

#         return render(request, template_name=self.template_name, context=context)

class BookmarkView(View):
    # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
    model = None
 
    def post(self, request, pk, id=0):
        print(f"DATA-FAVOURITE: {self}")
        user = auth.get_user(request)
        # пытаемся получить закладку из таблицы, или создать новую
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        # если не была создана новая закладка, 
        # то считаем, что запрос был на удаление закладки
        if not created:
            bookmark.delete()
 
        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
    
class LikekView(View):
    # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
    model = None
    model_notificate = None

    def post(self, request, pk, id=0):
        print(f"DATA-LIKE: {pk}")
        user = auth.get_user(request)

        # проверка на существование лайка
        like, created = self.model.objects.get_or_create(user=user, obj_id=pk)

        print(f"USER {like.obj.author}\nCREATOR {user}\nOBJ_ID {pk}")

        # проверка на существование уведомления
        notification, created_notificate = self.model_notificate.objects.get_or_create(
            user=like.obj.author,
            creator=user, obj_id=pk
        )

        print("MODEL-CLASS IS", like.obj)

        if not created:
            like.delete()

            like.obj.amount_of_likes -= 1
            like.obj.save()

        else:

            like.obj.amount_of_likes += 1
            like.obj.save()

        if not created_notificate:
            print("DELETED NOTIFICATION")
            notification.delete()

        print("NOTITFICATION", notification, notification.creator, self.model_notificate)

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )

# вход через telegram
def tele_entrance(request):

    # Initially, the index page may have no get params in URL
    # For example, if it is a home page, a user should be redirected from the widget
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')

    try:
        result = verify_telegram_authentication(
            bot_token=bot_token, request_data=request.GET
        )

    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')

    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')

    # Or handle it like you want. For example, save to DB. :)
    return HttpResponse('Hello, ' + result['first_name'] + '!')


# def tele_callback(request):
#     if request.method == "POST":
#         print("USER", request.user)
#         print("USER-ID", request.user.id)

#     telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

#     context = {'telegram_login_widget': telegram_login_widget}
    

#     return render(request, 'telegram_auth/callback.html', context)

# вход по редиректу через телеграмм
def tele_entrance(request):
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')

    try:
        result = verify_telegram_authentication(
            bot_token=bot_token, request_data=request.GET
        )

    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')

    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')

    # Or handle it like you want. For example, save to DB. :)
    # return HttpResponse('Hello, ' + result['first_name'] + '!')

    print("RESULT", result['username'], result['id'])

    user = auth.authenticate(username=result['username'], telegram_id=result['id'])

    # если пользователь с такими данными существует
    if user is not None:
        auth.login(request, user)

        return redirect('posts_feed')
    
    # если пользователя не существует, то зарегистрировать
