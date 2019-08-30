from django.contrib import admin
from .models import category, post, comment
# Register your models here.


class categoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName']


admin.site.register(category, categoryAdmin)
