# Generated by Django 3.2.12 on 2022-04-07 17:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('description', models.TextField()),
                ('link', models.URLField(max_length=1024)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='FeedLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rss_link', models.URLField(unique=True)),
            ],
        ),
    ]
