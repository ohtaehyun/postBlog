from django.contrib import admin
from .models import comuUser

# Register your models here.


class comuUserAdmin(admin.ModelAdmin):
    list_display = ['userId', 'userPassword', 'userEmail', 'signUpDate']


admin.site.register(comuUser, comuUserAdmin)
