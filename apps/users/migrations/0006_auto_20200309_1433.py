# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-03-09 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200228_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='user/%Y/%m', verbose_name='\u5934\u50cf'),
        ),
    ]