# Generated by Django 5.0.4 on 2025-01-27 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0025_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#EO28MP6R98', max_length=50),
        ),
    ]
