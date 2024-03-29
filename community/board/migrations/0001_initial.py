# Generated by Django 2.2.5 on 2019-09-10 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comuUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('categoryId', models.AutoField(primary_key=True, serialize=False, verbose_name='카테고리Id')),
                ('categoryName', models.TextField(max_length='30', unique=True, verbose_name='카테고리명')),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('postId', models.AutoField(primary_key=True, serialize=False, verbose_name='글번호')),
                ('postTitle', models.TextField(max_length='64', verbose_name='제목')),
                ('postContent', models.TextField(verbose_name='내용')),
                ('postedTime', models.DateField(auto_now_add=True, verbose_name='작성일')),
                ('editedTime', models.DateField(auto_now=True, verbose_name='수정일')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comuUser.CommuUser', verbose_name='작성자')),
                ('categoryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.category')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('commentId', models.AutoField(primary_key=True, serialize=False, verbose_name='댓글번호')),
                ('commentContent', models.TextField(max_length='150', verbose_name='댓글내용')),
                ('postedTime', models.DateField(auto_now_add=True, verbose_name='작성일')),
                ('editedTime', models.DateField(auto_now=True, verbose_name='수정일')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comuUser.CommuUser', verbose_name='작성자')),
                ('targetPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
        ),
    ]
