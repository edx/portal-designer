# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-22 12:38
from __future__ import unicode_literals

import designer.apps.branding.utils
from wagtail.images.models import Image
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('pages', '0015_enterprisepage_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisepagebranding',
            name='banner_background_color',
            field=models.CharField(blank=True, default='#FFFFFF', max_length=7, null=True, validators=[designer.apps.branding.utils.validate_hexadecimal_color]),
        ),
        migrations.AddField(
            model_name='programpagebranding',
            name='cover_image_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Cover Image'),
        ),
        migrations.AddField(
            model_name='programpagebranding',
            name='texture_image_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Texture Image'),
        ),
        migrations.DeleteModel(
            name='IndexPageBranding',
        ),
    ]
