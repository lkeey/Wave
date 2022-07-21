from django.contrib import admin
from .models import Post, Profile, LikePost

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
admin.site.register(LikePost)


