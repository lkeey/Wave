from django.db import models

from django.utils import timezone

from django.contrib.auth import get_user_model

from django.urls import reverse

from blog.models import Profile

User = get_user_model()

# Create your models here.


class ChatManager(models.Manager):
    def get_amount_unreaded(self):
        return super().get_queryset().filter(readable=False)

    def get_amount_unreaded_all(self):
        return super().get_queryset().filter(members__in=False)

    def get_earliest_message(self):
        return super().get_queryset().last()


class Chat(models.Model):
    
    DIALOG = 'D'
    CHAT = 'C'

    CHAT_CHOICES = (
        (DIALOG, "Dialog"),
        (CHAT, "Chat"),     
    )

    type = models.CharField(
        "Type",
        max_length=1,
        choices=CHAT_CHOICES,
        default=DIALOG,
    )

    members = models.ManyToManyField(
        User, verbose_name = "Participant"
    )


    # @models.permalink
    def get_absolute_url(self):
        # return 'users:messages', (), {'chat_id': self.pk }
        return reverse('messages', kwargs={"chat_id": self.pk})

class Group(models.Model):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    group = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="group",
    )

    name = models.TextField(
        '', blank=True,
        null=False, max_length=100,
    )

    bio = models.TextField(
        '', blank=True,
        null=False, max_length=200,
    )

    image = models.ImageField(
        upload_to='group_images', 
        default='profile_images/blank-profile-img.png'
    )

    def get_object(self, group):
        return Group.objects.filter(id=group).first()


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
 
    unreaded_objects = ChatManager()

    def __str__(self):
        return self.message
