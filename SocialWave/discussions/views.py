from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, ListView

from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
# https://docs.djangoproject.com/en/4.0/ref/contrib/
# messages/

from django.contrib import messages

from django.views.generic.dates import timezone_today
from discussions.models import Discussion

from . forms import DiscussionCreateForm

from django.contrib.auth.decorators import login_required

# Create your views here.

class UserDiscussionListView(ListView) :
    # Модель пост в models.py
    model = Discussion

    # Имя шаблона html
    template_name = 'discussions/user_discussions.html'

    def get_context_data(self, **kwargs):

        user = get_object_or_404(User,
            username = self.kwargs.get('username')
            )

        queryset = Discussion.objects.filter(author=user)

        context = super().get_context_data(**kwargs)

        context['discussions post_user_list'] = queryset.order_by('-date_created')
        
        return context

class DiscussionDetailtView(DetailView):
    model = Discussion

    template_name = 'discussions/discussion_detail.html'
    context_object_name = 'discussion_detail'

    # def get_pk(self):


@login_required
def discussion_create(request):
    print("USER", request.user)

    # если запрос POST. то тогда обрабатываем форму
    if request.method == 'POST':
        # Создадим экземпляр формы и заполним его данными запроса

        # Создадим форму для редактирования

        form = DiscussionCreateForm(request.POST, request.FILES)
        print(form) 
        # данные пост для заполнения формы

        if form.is_valid():
            new_disccusion = form.save(commit=False)
            new_disccusion.author = request.user
            new_disccusion.save()

            return redirect(new_disccusion.get_absolute_url())

    else:
        # если get-запрос, то вернуть пустую форму
        formset = DiscussionCreateForm()

    return render(request, 'discussions/create.html', {'formset': formset})
