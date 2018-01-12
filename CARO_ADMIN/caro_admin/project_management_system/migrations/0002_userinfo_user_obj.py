# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-19 08:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('project_management_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user_obj',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.User'),
        ),
    ]