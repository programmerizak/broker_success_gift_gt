# Generated by Django 5.0.4 on 2024-06-19 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#50D53TTVES', max_length=50),
        ),
    ]
