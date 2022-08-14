from pyexpat import model
from tkinter import N
from django.db import models
from django.conf import settings
from django.utils import timezone

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class FriendList(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="user"
    )

    friends = models.ManyToManyField(
        User,
        blank=True,
        related_name="friends"
    )

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        # Add a new friend

        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

            print(f"ADDING {self} - {account} - {self.friends.all()}")


    def remove_friend(self, account):
        # remove a friend

        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        # Initiate the action of unfriending someone
    
        remover_friends_list = self 

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friends from removee friend list
        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        # Is this a friend

        if friend in self.friends.all():
            return True

        return False

class FriendRequest(models.Model):
    """
    A friend request
        1. SENDER:
            Person sending request
        2. RECEIVER:
            Person receiving request 
    """

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sender"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receiver"
    )

    is_active = models.BooleanField(
        blank=True, 
        null=False, 
        default=True
    )

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        # Accept the friend request

        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)

            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)

                self.is_active = False
                self.save()

    def decline(self):
        # Decline a friend request

        self.is_active = False
        self.save()

    def cancel(self):
        # Cancel a friend request

        self.is_active = False
        self.save()
