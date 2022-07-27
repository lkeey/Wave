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


# <nav>
#     <ul class="topmenu">
#         {# All POSTS #}
#       <li>Your Activity
#         <ul class="submenu">
#             {% if blog_post_user_list|length > 0 %}
#             {% for post in blog_post_user_list %}
#                 <div class="post alert alert-info">
#                     <!-- DropDown -->
#                     <div class="dropdown" style="float:right;">
#                         <button class="dropbtn"><i class="fa-solid fa-bars"></i></button>
#                         <div class="dropdown-content">
#                           <a href="#"><i class="fa-solid fa-download"></i> Save</a>
#                           <a href="#"><i class="fa-solid fa-share-from-square"></i> Share</a>
#                           <a href="#"><i class="fa-solid fa-file-pen"></i> Edit</a>
#                           <a href="#"><i class="fa-solid fa-trash-can danger-icon"></i> Delete</a>
#                         </div>
#                     </div>
                    
#                     <div class="box">
#                         <div class="">
#                             <a href="{% url 'profile_user' user_name=post.author.username %}">
#                                 <img src="{{ post.author.profile.all.0.profile_img.url }}" alt="None" class="img-profile-comm">
#                             </a>
#                         </div>
#                         <div class="">
#                             <a href="{% url 'profile_user' user_name=post.author.username %}">
#                                 <p class="author">{{ post.author }}</p>
#                             </a>
#                         </div>
#                     </div>
        
#                     <h3 class="title">{{ post.title }}</h3>
        
#                     <a href="{{ post.image.url }}">
#                         <img src="{{ post.image.url }}" alt="None" class="post-image">
#                     </a>
                    
#                     <div class="content">@{{ post.author }}: {{ post.content|safe }}</div><br>
        
#                     <p class="date">{{ post.date_created }}</p><br>
                    
#                     <div class="py-3 px-4 space-y-3 box"> 
                                       
#                         <div data-type="post" data-id="{{ post.id }}" data-action="like" class="flex space-x-4 lg:font-bold data-likes text-center">
#                             <a href="">
#                                 <div class="p-2 rounded-full text-black " >
#                                 <!-- <span class="glyphicon glyphicon-star">Count: </span> -->
#                                 <!-- <span data-count="like">{{ post.amount_of_likes }}</span> -->
                                
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="25" height="25" class="">
#                                         <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
#                                     </svg>
                                    
#                                     <!-- {% if post.amount_of_likes == 0 %}
#                                     <p>No likes</p>
                                    
#                                     {% elif post.amount_of_likes == 1 %}
                                    
#                                     <p>Liked by {{post.amount_of_likes}} person</p>
#                                     <p data-count="like"></p>
                                    
#                                     {% else %}
#                                     <p data-count="like">Liked by {{post.amount_of_likes}} people</p>
                                    
#                                     {% endif %} -->
                                    
#                                     <p>Liked by </p>
#                                     <p data-count="like">{{post.amount_of_likes}}</p>
#                                     <p>people</p>
#                                 </div>   
#                              </a>
#                         </div>
        
#                         <div class="data-comm text-center">
        
#                             <a href="{% url 'discussions_detail' pk=post.pk %}">
#                                 <div class="p-2 rounded-full text-black " >
#                                     <i class="fa-solid fa-comment-dots comment-icon"></i>
#                                     {% if post.amount_of_comments == 0 %}
#                                     <p>No Comments</p>
#                                     {% elif post.amount_of_comments == 1 %}
#                                     <p>Commented by {{post.amount_of_comments}} person</p>
#                                     {% else %}
#                                     <p>Commented by {{post.amount_of_comments}} people</p>
#                                     {% endif %}
#                                 </div>  
#                             </a>
        
#                         </div>
#                         <div data-id="{{ post.id }}" data-type="post" data-action="bookmark" title="Favourite" class="data-save text-center">
#                             <a href="">
#                                 <span class="glyphicon glyphicon-star"><i class="fa-solid fa-bookmark"></i> </span>
#                                 <span data-count="bookmark">{{ post.get_bookmark_count }}</span>
#                             </a>
                            
#                         </div>
#                     </div>
#                 </div>
#             {% endfor %}
        
#         {% else %}
        
#         <h3 class="title">You haven't got any post...</h3>
        
#         {% endif %}
         
#         </ul>
#       </li>
#       <li>HI
#         <ul class="submenu">
#             {% if blog_post_user_list|length > 0 %}
#             {% for post in blog_post_user_list %}
#                 <div class="post alert alert-info">
#                     <!-- DropDown -->
#                     <div class="dropdown" style="float:right;">
#                         <button class="dropbtn"><i class="fa-solid fa-bars"></i></button>
#                         <div class="dropdown-content">
#                           <a href="#"><i class="fa-solid fa-download"></i> Save</a>
#                           <a href="#"><i class="fa-solid fa-share-from-square"></i> Share</a>
#                           <a href="#"><i class="fa-solid fa-file-pen"></i> Edit</a>
#                           <a href="#"><i class="fa-solid fa-trash-can danger-icon"></i> Delete</a>
#                         </div>
#                     </div>
                    
#                     <div class="box">
#                         <div class="">
#                             <a href="{% url 'profile_user' user_name=post.author.username %}">
#                                 <img src="{{ post.author.profile.all.0.profile_img.url }}" alt="None" class="img-profile-comm">
#                             </a>
#                         </div>
#                         <div class="">
#                             <a href="{% url 'profile_user' user_name=post.author.username %}">
#                                 <p class="author">{{ post.author }}</p>
#                             </a>
#                         </div>
#                     </div>
        
#                     <h3 class="title">{{ post.title }}</h3>
        
#                     <a href="{{ post.image.url }}">
#                         <img src="{{ post.image.url }}" alt="None" class="post-image">
#                     </a>
                    
#                     <div class="content">@{{ post.author }}: {{ post.content|safe }}</div><br>
        
#                     <p class="date">{{ post.date_created }}</p><br>
                    
#                     <div class="py-3 px-4 space-y-3 box"> 
                                       
#                         <div data-type="post" data-id="{{ post.id }}" data-action="like" class="flex space-x-4 lg:font-bold data-likes text-center">
#                             <a href="">
#                                 <div class="p-2 rounded-full text-black " >
#                                 <!-- <span class="glyphicon glyphicon-star">Count: </span> -->
#                                 <!-- <span data-count="like">{{ post.amount_of_likes }}</span> -->
                                
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="25" height="25" class="">
#                                         <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
#                                     </svg>
                                    
#                                     <!-- {% if post.amount_of_likes == 0 %}
#                                     <p>No likes</p>
                                    
#                                     {% elif post.amount_of_likes == 1 %}
                                    
#                                     <p>Liked by {{post.amount_of_likes}} person</p>
#                                     <p data-count="like"></p>
                                    
#                                     {% else %}
#                                     <p data-count="like">Liked by {{post.amount_of_likes}} people</p>
                                    
#                                     {% endif %} -->
                                    
#                                     <p>Liked by </p>
#                                     <p data-count="like">{{post.amount_of_likes}}</p>
#                                     <p>people</p>
#                                 </div>   
#                              </a>
#                         </div>
        
#                         <div class="data-comm text-center">
        
#                             <a href="{% url 'discussions_detail' pk=post.pk %}">
#                                 <div class="p-2 rounded-full text-black " >
#                                     <i class="fa-solid fa-comment-dots comment-icon"></i>
#                                     {% if post.amount_of_comments == 0 %}
#                                     <p>No Comments</p>
#                                     {% elif post.amount_of_comments == 1 %}
#                                     <p>Commented by {{post.amount_of_comments}} person</p>
#                                     {% else %}
#                                     <p>Commented by {{post.amount_of_comments}} people</p>
#                                     {% endif %}
#                                 </div>  
#                             </a>
        
#                         </div>
#                         <div data-id="{{ post.id }}" data-type="post" data-action="bookmark" title="Favourite" class="data-save text-center">
#                             <a href="">
#                                 <span class="glyphicon glyphicon-star"><i class="fa-solid fa-bookmark"></i> </span>
#                                 <span data-count="bookmark">{{ post.get_bookmark_count }}</span>
#                             </a>
                            
#                         </div>
#                     </div>
#                 </div>
#             {% endfor %}
        
#         {% else %}
        
#         <h3 class="title">You haven't got any post...</h3>
        
#         {% endif %}
     
        
#         </ul>
#       </li>
     
#     </ul>
#   </nav>
