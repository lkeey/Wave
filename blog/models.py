# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
import pytz

from django.urls import reverse

from ckeditor.fields import RichTextField

from pytils.translit import slugify

from datetime import datetime

from django.contrib.auth import get_user_model

from PIL import Image

from django.contrib.postgres.fields import ArrayField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
# django.template.defaultfilters import slugify
# from django.utils.text import slugify

User = get_user_model()


class Profile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    id_user = models.IntegerField()
    
    bio = models.TextField(blank=True)
    
    telegram_id = models.IntegerField(default=0)

    profile_img = models.ImageField(
        upload_to='profile_images', 
        default='blank-profile-img.png'
        )
    
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    # возвращает количество уведомлений
    def get_amount_notifications(self):
        likes = NotificationLike.objects.filter(user=self.user, readable=False).count()
        comms = NotificationComment.objects.filter(user=self.user, readable=False).count()
        comms_created = NotificationCommentCreated.objects.filter(user=self.user, readable=False).count()
        
        return likes + comms + comms_created

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_img.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)


class Post(models.Model):

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    author = models.ForeignKey(User,
                on_delete=models.CASCADE,
    )


    title = models.CharField('',max_length=200,
        # help_text='No more 200 symbols',
        db_index=True,
    )

    image = models.ImageField(upload_to='post_images')

    content = RichTextField('', blank=True, null=True,
                    max_length=5000,
                    
            )

    date_created = models.DateTimeField(default=datetime.now)

    date_updated = models.DateTimeField(auto_now=True)

    amount_of_likes = models.IntegerField(default=0)

    amount_of_comments = models.IntegerField(default=0)

    slug = models.SlugField(max_length=50) # unique=True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        print("PK", self.pk)
        return reverse('discussions_detail', kwargs={"pk": self.pk})

    def get_bookmark_count(self):
        return self.bookmarkpost_set.all().count()

    def save(self):
        super().save()
        if self.image:
            print("Pruning")
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Comment(models.Model):
    class Meta:
        db_table = "comments"
 
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments_post'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )

    amount_of_likes = models.IntegerField(default=0)
    
    content = models.TextField('')

    create_date = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.content[0:200]
 

# BOOKMARKS

class BookmarkBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
 
    def __str__(self):
        return self.user.username


class BookmarkPost(BookmarkBase):
    class Meta:
        db_table = "bookmark_post"
 
    obj = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

class BookmarkComment(BookmarkBase):
    class Meta:
        db_table = "bookmark_comment"
 
    obj = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )

# class LikePost(models.Model):
    # post_id = models.CharField(max_length=500)
    # username = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.username
 
# LIKES

class LikesBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,    
    )
 
    def __str__(self):
        return self.user.username

class PostLike(LikesBase):
    class Meta:
        db_table = "like_post"

    obj = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
 
class CommentLike(LikesBase):
    class Meta:
        db_table = "like_comment"
 
    obj = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )

# NOTIFICATIONS

class NotitificationBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  
        related_name="%(app_label)s_%(class)s_user", 
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_creator",  
    )

    readable = models.BooleanField(default=False)

    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username

class NotificationLike(NotitificationBase):
    class Meta:
        db_table = "notificate_like_post"

    obj = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    
class NotificationComment(NotitificationBase):
    class Meta:
        db_table = "notificate_comment_post"

    obj = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="user_notifications_like"
    )

class NotificationCommentCreated(NotitificationBase):
    class Meta:
        db_table = "notificate_comment_post_created"

    obj = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="user_notifications_comm"
    )

