# Generated by Django 3.2.25 on 2024-04-07 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#BMO0F7VH8Y', max_length=50),
        ),
    ]
