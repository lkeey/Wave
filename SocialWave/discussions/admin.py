from django.contrib import admin
from discussions.models import Discussion

# Register your models here.
@admin.register(Discussion)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created', 'date_updated']
    
    # автозаполнение
    prepopulated_fields = {
        "slug": ('title',),
    }