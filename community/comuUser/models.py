from django.db import models

# Create your models here.


class comuUser(models.Model):
    userId = models.CharField(max_length=32, verbose_name="사용자명")
    userPassword = models.CharField(max_length=32, verbose_name="사용자암호")
    signUpDate = models.DateField(auto_now=True, verbose_name="가입일")
    userEmail = models.EmailField(max_length=60, verbose_name="이메일")

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "comuUser"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"
