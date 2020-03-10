# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-03-08 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_lesson_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='\u8bbf\u95ee\u5730\u5740'),
        ),
    ]