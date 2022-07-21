from pickletools import read_uint1

from django.http.response import HttpResponseRedirect

from django.urls.base import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, ListView

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User, auth

from django.contrib.auth.mixins import LoginRequiredMixin
# https://docs.djangoproject.com/en/4.0/ref/contrib/
# messages/

from django.contrib import messages

from django.views.generic.dates import timezone_today
from .models import Post, Profile, LikePost

from .forms import PostCreateForm

from django.contrib.auth.decorators import login_required

# Create your views here.

class UserPostsListView(ListView):
    # Модель пост в models.py
    model = Post

    # Имя шаблона html
    template_name = 'discussions/user_discussions.html'

    def get_context_data(self, **kwargs):

        user = get_object_or_404(User,
            username = self.kwargs.get('username')
            )

        queryset = Post.objects.filter(author=user)

        context = super().get_context_data(**kwargs)

        context['discussions post_user_list'] = queryset.order_by('-date_created')
        
        return context

class PostDetailtView(DetailView):
    model = Post

    template_name = 'discussions/discussion_detail.html'
    context_object_name = 'discussion_detail'

    # def get_pk(self):


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

        queryset = Post.objects.filter(author=user).order_by('-date_created')
        
        # context = super().get_context_data(**kwargs)['blog_post_user_list'] = queryset
        context = {
            'blog_post_user_list': queryset,
        }
        return context

# все посты
def feed(request):
    data = {
        "all_posts": Post.objects.order_by('-date_created'),
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
                return redirect('settings')


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

@login_required(login_url='sign_in') 
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(
        post_id=post_id,
        username=username
    ).first()

    if like_filter == None:
        new_like = LikePost.objects.create(
            post_id=post_id,
            username=username
        )

        new_like.save()

        post.amount_of_likes += 1
        post.save()

        return redirect('posts_feed')

    else:
        like_filter.delete()
        post.amount_of_likes -= 1
        post.save()
        return redirect('posts_feed')


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