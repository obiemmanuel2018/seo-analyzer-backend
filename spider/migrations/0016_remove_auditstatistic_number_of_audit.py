# Generated by Django 4.0.4 on 2022-06-08 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0015_remove_crawlingstatistic_number_of_crawl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditstatistic',
            name='number_of_audit',
        ),
    ]
