# Generated by Django 5.0.4 on 2025-01-23 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0023_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#SCN02EC8GY', max_length=50),
        ),
    ]
