# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 09:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0007_auto_20161208_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmarks',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='bookmarks',
            name='user_name',
        ),
        migrations.DeleteModel(
            name='Bookmarks',
        ),
    ]