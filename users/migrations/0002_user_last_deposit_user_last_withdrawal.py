# Generated by Django 5.0.4 on 2025-01-17 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_deposit',
            field=models.CharField(default='N/A', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='last_withdrawal',
            field=models.CharField(default='N/A', max_length=20),
        ),
    ]
