# Generated by Django 5.0.4 on 2025-01-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0022_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#DCZTNIXNJL', max_length=50),
        ),
    ]
