# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 04:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0005_professor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('alma_mater', models.CharField(max_length=120, null=True)),
                ('about', models.CharField(max_length=120, null=True)),
                ('contact_info', models.CharField(max_length=120, null=True)),
            ],
        ),
    ]
