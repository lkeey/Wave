from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404

from blog.models import Post

from discussions.models import Discussion

from django.contrib.auth.models import User
# Create your views here.

class UserMixin(object):
    # выборка пользователя
    pass

# for profile
class UserPostListView(ListView):
    # model in models.py
    model = Post

    # name of template
    template_name = 'blog/profile.html'

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

        queryset = Discussion.objects.filter(author=user).order_by('-date_created')
        
        # context = super().get_context_data(**kwargs)['blog_post_user_list'] = queryset
        context = {
            'blog_post_user_list': queryset,
        }
        return context


# все посты
def feed(request):
    data = {
        "all_posts": Discussion.objects.order_by('-date_created'),
    }

    return render(request, 'blog/posts_feed.html', data)
