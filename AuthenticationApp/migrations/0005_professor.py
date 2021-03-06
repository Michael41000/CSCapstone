# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0004_auto_20161120_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120, null=True)),
                ('last_name', models.CharField(max_length=120, null=True)),
                ('university', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
            ],
        ),
    ]
