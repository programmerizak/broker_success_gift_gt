# Generated by Django 5.0.4 on 2025-01-23 05:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0005_alter_currency_barcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='percentage_deposit_fee',
            field=models.DecimalField(decimal_places=8, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
