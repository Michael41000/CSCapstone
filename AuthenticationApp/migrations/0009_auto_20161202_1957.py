# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 19:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0008_professor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engineer',
            name='about',
        ),
        migrations.RemoveField(
            model_name='engineer',
            name='alma_mater',
        ),
        migrations.RemoveField(
            model_name='engineer',
            name='contact_info',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='contact_info',
        ),
        migrations.RemoveField(
            model_name='professor',
            name='university',
        ),
    ]
