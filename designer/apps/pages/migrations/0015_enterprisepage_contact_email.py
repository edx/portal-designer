# Generated by Django 1.11.23 on 2019-08-30 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_enterprisepage_enterprisepagebranding'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisepage',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Learning Coordinator Email Address'),
        ),
    ]