# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 18:14
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('contact', models.CharField(max_length=11)),
                ('aadhaar', models.CharField(blank=True, max_length=12, null=True)),
                ('bhamashah', models.CharField(blank=True, max_length=12, null=True)),
                ('birth_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'Citizen',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
