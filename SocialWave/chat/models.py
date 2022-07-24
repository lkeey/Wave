from django.db import models
import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model

from blog.models import Profile

User = get_user_model()

# Create your models here.
class Room(models.Model):
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    # DIALOG = 'D'
    # CHAT = 'C'
    # CHAT_TYPE_CHOICES = (
    #     (DIALOG, ('Dialog')),
    #     (CHAT, ('Chat'))
    # )

    # user_1 = models.ForeignKey(User,
    #             on_delete=models.CASCADE,
    # )

    # user_2 = models.ForeignKey(User,
    #             on_delete=models.CASCADE,
    # )

    # type = models.CharField(
    #     max_length=1,
    #     choices=CHAT_TYPE_CHOICES,
    #     default=DIALOG
    # )

    members = models.ManyToManyField(User, verbose_name=("Участник"))

    # def __str__(self):
    #     return self.user_1, self.user_2

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    # user = models.CharField(max_length=1000000)

    # chat = models.ForeignKey(
    #     Room, 
    #     verbose_name=("Чат"),
    #     on_delete=models.CASCADE,
    #     )
    
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    # )

    is_readed = models.BooleanField(default=False)

    # room = models.CharField(max_length=1000000)
     

