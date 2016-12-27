# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-26 12:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='viewers',
        ),
        migrations.AddField(
            model_name='post',
            name='latest_replier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lst_replier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='repliers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='voter_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pstauthor', to=settings.AUTH_USER_MODEL),
        ),
    ]
