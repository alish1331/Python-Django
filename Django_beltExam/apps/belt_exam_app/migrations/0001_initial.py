# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-23 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_text', models.TextField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quoted_by', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=45, null=True)),
                ('email', models.CharField(max_length=45, null=True)),
                ('password', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes_posted', to='belt_exam_app.User'),
        ),
        migrations.AddField(
            model_name='quote',
            name='favouriting_users',
            field=models.ManyToManyField(related_name='favourite_quotes', to='belt_exam_app.User'),
        ),
    ]
