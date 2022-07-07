from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

# модель поста
class Post(models.Model):

    # названия
    class Meta:
        verbose_name = 'Creating Post'
        verbose_name_plural = 'Creating Posts'

    # поля модели
    title = models.CharField(max_length=200, 
                     help_text='200 symbols is max',
                     db_index=True,
    )
    # content = models.TextField(max_length=2000, 
    #                 # можно записывать или не записывать
    #                     blank=True,
    #                     null=True,
    #                     help_text='5000 symbols is max',
    # )               
    content = RichTextField(max_length=2000, 
                    # можно записывать или не записывать
                        blank=True,
                        null=True,
                        help_text='5000 symbols is max',
    )               

    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )

    # в url при использовании slug обязательно добавлять id + get_absolute_url()
    slug = models.SlugField(max_length=50)# unique = True

    # для лайков записи
    likes = models.ManyToManyField(
        User,
        related_name='postcomment',
        blank=True,
        default=0,
    )

    # для ответов на комменты
    reply = models.ForeignKey(
        'self',
        null=True,
        related_name='reply_ok',
        on_delete=models.CASCADE,
        default=None
    )

    # подсчитывает все лайки на посте
    def total_likes(self):
        return self.likes.count()

    # дает индивидуальную ссылку для каждого поста
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})

    # возвращает заголовок поста в admin-ку
    def __str__(self):
        return self.title