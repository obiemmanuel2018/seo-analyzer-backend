# Generated by Django 4.0.4 on 2022-06-01 11:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0009_alter_result_duplicate_descriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='duplicate_descriptions',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=8),
        ),
        migrations.AlterField(
            model_name='result',
            name='duplicate_h1',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=8),
        ),
        migrations.AlterField(
            model_name='result',
            name='duplicate_titles',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=8),
        ),
    ]
