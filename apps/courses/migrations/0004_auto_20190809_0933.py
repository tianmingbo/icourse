# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-08-09 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=20, verbose_name='课程类别'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='老师告诉你'),
        ),
        migrations.AddField(
            model_name='course',
            name='you_need_know',
            field=models.CharField(default='', max_length=300, verbose_name='课程须知'),
        ),
    ]