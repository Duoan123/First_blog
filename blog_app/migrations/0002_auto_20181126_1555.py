# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-26 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
