# Generated by Django 5.0.4 on 2024-07-02 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#KWL2DLWM9G', max_length=50),
        ),
    ]
