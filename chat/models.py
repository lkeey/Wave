from django.db import models

from django.utils import timezone

from django.contrib.auth import get_user_model

from django.urls import reverse

from blog.models import Profile

User = get_user_model()

# Create your models here.

class Chat(models.Model):
    # DIALOG = 'D'
    # CHAT = 'C'
    # CHAT_CHOICES = (
    #     (DIALOG, _('Dialog')),
    #     (CHAT, _('Chat'))
    # )

    CHAT_CHOICES = (
        ("D", "Dialog"),
        ("C", "Chat"),     
    )

    type = models.CharField(
        "Type",
        max_length=1,
        choices=CHAT_CHOICES,
        default="D",
    )

    members = models.ManyToManyField(
        User, verbose_name = "Participant"
    )
 
    # @models.permalink
    def get_absolute_url(self):
        # return 'users:messages', (), {'chat_id': self.pk }
        return reverse('messages', kwargs={"chat_id": self.pk})

 
class Message(models.Model):
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    message = models.TextField(
        '', blank=True, 
        null=False, max_length=1000,
    )
    
    date_created = models.DateTimeField(default=timezone.now)
    
    readable = models.BooleanField(default=False)
 
 
    def __str__(self):
        return self.message
