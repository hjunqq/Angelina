# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DayMood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('score', models.IntegerField()),
                ('content', models.CharField(max_length=100000, blank=b'true')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DayScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('score', models.FloatField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('moods', models.ManyToManyField(to='diary.DayMood')),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('addtime', models.DateTimeField(blank=b'true')),
                ('text', models.CharField(unique=True, max_length=150)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='MonthScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('score', models.FloatField(null=b'true')),
                ('tscore', models.FloatField(null=b'true')),
                ('count', models.IntegerField(null=b'true')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLogInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logInIP', models.CharField(max_length=150)),
                ('logInTime', models.DateTimeField()),
                ('logOutTime', models.DateTimeField()),
                ('UserAgent', models.CharField(max_length=150)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserLogInfo',
                'verbose_name_plural': 'UserLogInfoes',
            },
        ),
        migrations.CreateModel(
            name='YearScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('score', models.FloatField(null=b'true')),
                ('tscore', models.FloatField(null=b'true')),
                ('count', models.IntegerField(null=b'true')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='daymood',
            name='keywords',
            field=models.ManyToManyField(to='diary.KeyWord'),
        ),
    ]
