# Generated by Django 2.2.4 on 2019-08-28 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete='models.CASCADE', to='comuUser.CommuUser', verbose_name='작성자'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comuUser.CommuUser', verbose_name='작성자'),
        ),
    ]
