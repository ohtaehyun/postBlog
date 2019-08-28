from django.contrib import admin
from .models import CommuUser

# Register your models here.


class comuUserAdmin(admin.ModelAdmin):
    list_display = ['userName', 'userEmail', 'userPassword']


admin.site.register(CommuUser, comuUserAdmin)
