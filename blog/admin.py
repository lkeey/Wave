from django.contrib import admin
from .models import (
    Post, Profile, 
    PostLike, Comment,
    BookmarkPost,
    BookmarkComment,
    CommentLike,
    NotificationLike,
    NotificationComment,
)

# Register your models here.
@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'date_updated', 'amount_of_likes']
    
    # автозаполнение
    prepopulated_fields = {
        "slug": ('title',),
    }
    
# admin.site.register(Discussion)

admin.site.register(Profile)

admin.site.register(Comment)

admin.site.register(BookmarkPost)
admin.site.register(PostLike)

admin.site.register(CommentLike)
admin.site.register(BookmarkComment)

admin.site.register(NotificationLike)
admin.site.register(NotificationComment)


