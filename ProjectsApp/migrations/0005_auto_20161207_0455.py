# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 04:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0004_auto_20161207_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='yearsXP',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
    ]
