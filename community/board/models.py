from django.db import models

# Create your models here.


class category(models.Model):
    categoryId = models.AutoField(primary_key=True, verbose_name="카테고리Id")
    categoryName = models.TextField(
        max_length="30", verbose_name="카테고리명", unique=True)


class post(models.Model):
    postId = models.AutoField(primary_key=True, verbose_name="글번호")
    postTitle = models.TextField(max_length="64", verbose_name="제목")
    postContent = models.TextField(verbose_name="내용")
    postedTime = models.DateField(verbose_name="작성일", auto_now_add=True)
    editedTime = models.DateField(verbose_name="수정일", auto_now=True)
    author = models.ForeignKey(
        "comuUser.CommuUser", verbose_name=("작성자"), on_delete=models.CASCADE)
    categoryId = models.ForeignKey(category, on_delete="models.CASCADE")


class comment(models.Model):
    commentId = models.AutoField(primary_key=True, verbose_name="댓글번호")
    commentContent = models.TextField(max_length="150", verbose_name="댓글내용")
    targetPost = models.ForeignKey(post, on_delete="models.CASCADE")
    author = models.ForeignKey(
        "comuUser.CommuUser", verbose_name="작성자", on_delete="models.CASCADE")
    postedTime = models.DateField(verbose_name="작성일", auto_now_add=True)
    editedTime = models.DateField(verbose_name="수정일", auto_now=True)
