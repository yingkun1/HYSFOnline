# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-02-23 11:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='mobILe',
            new_name='mobile',
        ),
    ]