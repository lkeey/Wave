# -*- coding: utf-8 -*-

from tkinter import CASCADE
from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

from django.urls import reverse

from ckeditor.fields import RichTextField

from pytils.translit import slugify

from datetime import datetime

from django.contrib.auth import get_user_model

import uuid

from django.contrib.postgres.fields import ArrayField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
# django.template.defaultfilters import slugify
# from django.utils.text import slugify

User = get_user_model()

# class Discussion(models.Model):

#     class Meta:
#         verbose_name = 'Discussion'
#         verbose_name_plural = 'Discussions'

#     title = models.CharField(max_length=200,
#         help_text='No more 200 symbols',
#         db_index=True,
#         )

#     content = RichTextField(blank=True, null=True,
#                     max_length=5000,
#                     help_text="No more 5000 symbols",
#             )

#     date_created = models.DateTimeField(default=datetime.now)
    
#     date_updated = models.DateTimeField(auto_now=True)

#     author = models.ForeignKey(User,
#                 on_delete=models.CASCADE,
#                 )
#     slug = models.SlugField(max_length=50) # unique=True

#     likes = models.ManyToManyField(
#                     User, related_name='discussion_likes', 
#                     blank=True,
#                     verbose_name='Likes',
#                     )
#     saves_discussion = models.ManyToManyField(
#             User, related_name="blog_discussion_save",
#             blank=True,
#             verbose_name='Saved posts' 
#             )

#     def save(self, *args, **kwargs):

#         self.slug = slugify(self.title)

#         # Post.objects.create(
#         #     title=self.title,
#         #     content=self.content,
#         #     author=self.author,
#         #     slug=self.slug,
#         # ) 
        
#         super(Discussion, self).save(*args, **kwargs)

#         print("All Okey")

#     def total_likes(self):
#         return self.likes.count()

#     def total_saves_discussions(self):
#         return self.saves_posts.count()

#     def get_absolute_url(self):
#         print("PK", self.pk)
#         return reverse('discussions_detail', kwargs={"pk": self.pk})

#     def __str__(self):
#         return self.title

class Profile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    id_user = models.IntegerField()
    
    bio = models.TextField(blank=True)
    
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-img.png')
    
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    author = models.ForeignKey(User,
                on_delete=models.CASCADE,
                )


    title = models.CharField(max_length=200,
        help_text='No more 200 symbols',
        db_index=True,
    )

    image = models.ImageField(upload_to='post_images')

    content = RichTextField(blank=True, null=True,
                    max_length=5000,
                    help_text="No more 5000 symbols",
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