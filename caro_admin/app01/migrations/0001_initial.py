# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-19 08:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='用户组')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('email', models.CharField(blank=True, max_length=32, null=True, verbose_name='邮箱')),
                ('user2group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.UserGroup', verbose_name='用户组')),
                ('user2role', models.ManyToManyField(blank=True, null=True, to='app01.Role', verbose_name='角色')),
            ],
        ),
    ]
