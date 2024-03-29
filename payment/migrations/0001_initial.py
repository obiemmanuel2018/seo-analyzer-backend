# Generated by Django 4.0.4 on 2022-06-28 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('account_type', models.CharField(choices=[('free', 'free'), ('paid', 'paid')], default='free', max_length=100)),
                ('subscription_type', models.CharField(choices=[('free', 'free'), ('month', 'month'), ('year', 'year')], default='free', max_length=100)),
                ('payment_method', models.CharField(choices=[('empty', 'empty'), ('orange momo', 'orange momo'), ('mtn momo', 'mtn momo')], default='empty', max_length=100)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
