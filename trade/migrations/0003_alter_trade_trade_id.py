# Generated by Django 3.2.25 on 2024-04-07 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='#PD7D50PA92', max_length=50),
        ),
    ]
