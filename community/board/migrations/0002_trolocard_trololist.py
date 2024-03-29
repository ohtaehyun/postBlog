# Generated by Django 2.2.5 on 2019-09-10 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comuUser', '0001_initial'),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='troloList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listTitle', models.TextField(max_length='32', verbose_name='리스트 제목')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comuUser.CommuUser', verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='troloCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardTitle', models.TextField(max_length='32', verbose_name='카드 제목')),
                ('cardDescription', models.TextField(max_length='150', verbose_name='카드 설명')),
                ('targetList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.troloList', verbose_name='타겟 리스트')),
            ],
        ),
    ]
