from django.contrib import admin
from .models import category, post, comment
# Register your models here.


class categoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName']


admin.site.register(category, categoryAdmin)


class postAdmin(admin.ModelAdmin):
    list_display = ['postId', 'postTitle', 'postContent',
                    'postedTime', 'editedTime', 'author', 'categoryId']


admin.site.register(post, postAdmin)


class commentAdmin(admin.ModelAdmin):
    list_display = ['commentId', 'commentContent',
                    'targetPost', 'author', 'postedTime', 'editedTime']


admin.site.register(comment, commentAdmin)
