# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-19 15:15
from __future__ import unicode_literals


from django.db import migrations

def create_observers_group(apps, schema_editor, *args, **kwargs):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    Observers_group = Group.objects.create(name='Observers')
    access_admin = Permission.objects.get(codename='access_admin')
    Observers_group.permissions.add(access_admin)

def delete_observers_group(apps, schema_editor, *args, **kwargs):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get(name='Observers').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('wagtailadmin', '0001_create_admin_access_permissions'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_observers_group, delete_observers_group),
    ]
