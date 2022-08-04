from operator import length_hint
from pickletools import read_uint1

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

from django.http import HttpResponse

from django.contrib import messages

from django.views.generic.dates import timezone_today
from .models import (
    Post, Profile, 
    PostLike, CommentLike,
    BookmarkComment, BookmarkPost,
)

from .forms import PostCreateForm, CommentForm

from django.contrib.auth.decorators import login_required

import json

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

            return redirect(new_disccusion.get_absolute_url())

    
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
        user = get_object_or_404(
            User, 
            username=self.kwargs.get('username')
        )

        user_profile = Profile.objects.get(user=user)

        queryset_posts = Post.objects.filter(author=user).order_by('-date_created')
        
        query_posts_likes = PostLike.objects.filter(user=user).order_by('-obj')

        query_comm_likes = CommentLike.objects.filter(user=user).order_by('-obj')

        query_posts_favourite = BookmarkPost.objects.filter(user=user).order_by('-obj')

        # query_comm_favourite = BookmarkComment.objects.filter(user=user).order_by('-obj')

        # context = super().get_context_data(**kwargs)['blog_post_user_list'] = queryset
        context = {
            'blog_post_user_list': queryset_posts,

            'like_post_user_list': query_posts_likes,
            'like_comm_user_list': query_comm_likes,

            'favourite_post_user_list': query_posts_favourite,
            # 'favourite_comm_user_list': query_comm_favourite,

            'user_profile': user_profile,
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

        return redirect('user_posts_list', username=request.user)

# все посты
def feed(request):
    
    data = {
        "all_posts": Post.objects.order_by('-date_created'),
        "form": CommentForm
    }

    return render(request, 'discussions/posts_feed.html', data)

# registration
def sign_up(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if len(username) >= 3 and len(password) >= 8:


                if User.objects.filter(email=email).exists():
                    messages.info(request, "EMAIL WAS TAKEN")
                    return redirect('sign_up')

                elif User.objects.filter(username=username).exists():
                    messages.info(request, "USERANAME WAS TAKEN")

                else:
                    # create User
                    user = User.objects.create_user(
                        username=username,
                        email=email,
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
                        id_user=user_model.id                            
                    )

                    new_profile.save()
                    return redirect('posts_feed')
                    
            else:
                messages.info(request, 'The USERNAME must be more than 2 characters and the PASSWORD more than 7')


        else:
            messages.info(request, 'PASSWORD IS NOT MATCHING')
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

            return redirect('posts_feed')

        else:
            messages.info(request, 'DATA IS INVALID')

        

    return render(request, "discussions/sign_in.html")


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


def profile_user(request, user_name):

    # user_object = User.objects.get(username=pk)

    user = get_object_or_404(
            User, 
            username=user_name
        )

    user_profile = Profile.objects.get(user=user)

    user_posts = Post.objects.filter(author=user).order_by('-date_created')

    user_posts_length = len(user_posts)

    context = {
        'user_object': user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
    }

    return render(request, 'discussions/profile_user.html', context)


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
 
    def post(self, request, pk, id=0):
        print(f"DATA-LIKE: {pk}")
        user = auth.get_user(request)

        like, created = self.model.objects.get_or_create(user=user, obj_id=pk)

        print("MODEL-CLASS IS", like.obj)


        if not created:
            like.delete()

            like.obj.amount_of_likes -= 1
            like.obj.save()

        else:

            like.obj.amount_of_likes += 1
            like.obj.save()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
