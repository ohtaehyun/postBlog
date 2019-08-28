from django.db import models

# Create your models here.


class CommuUser(models.Model):
    userName = models.TextField(
        verbose_name="사용자 이름", unique="True", max_length="64")
    userEmail = models.TextField(
        verbose_name="사용자 Email", unique="True", max_length="64")
    userPassword = models.TextField(
        verbose_name="사용자 비밀번호", unique="True", max_length="64")
