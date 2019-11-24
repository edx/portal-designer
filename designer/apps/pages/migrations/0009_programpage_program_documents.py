# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-11 20:08
from __future__ import unicode_literals

from django.db import migrations
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20190708_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='programpage',
            name='program_documents',
            field=wagtail.core.fields.StreamField((('file', wagtail.core.blocks.StructBlock((('display_text', wagtail.core.blocks.CharBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())), icon='doc-full')), ('link', wagtail.core.blocks.StructBlock((('display_text', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock())), icon='link'))), blank=True, verbose_name='Program Documents'),
        ),
    ]
