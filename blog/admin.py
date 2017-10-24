from django.contrib import admin
from  .models import Post, Comment
# Register your models here.

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'message']
    list_display_links = ['id', 'message']
