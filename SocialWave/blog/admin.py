from django.contrib import admin
from blog.models import Post

# Register your models here.

# add class to admin page
# admin.site.register(Post)

@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created', 'date_updated']
    
    # автозаполнение
    prepopulated_fields = {
        "slug": ('title',),
    }
