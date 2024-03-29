# Generated by Django 1.11.22 on 2019-07-16 20:48

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_programpage_idp_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField(default=True, verbose_name='Display Program Documents')),
                ('header', models.CharField(default='Program Documents', max_length=128, verbose_name='Header for Program Documents')),
                ('documents', wagtail.fields.StreamField((('file', wagtail.blocks.StructBlock((('display_text', wagtail.blocks.CharBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())), icon='doc-full')), ('link', wagtail.blocks.StructBlock((('display_text', wagtail.blocks.CharBlock()), ('url', wagtail.blocks.URLBlock())), icon='link'))), blank=True, verbose_name='Documents', use_json_field=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='programpage',
            name='program_documents',
        ),
        migrations.AddField(
            model_name='programdocuments',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_documents', to='pages.ProgramPage', unique=True),
        ),
    ]
