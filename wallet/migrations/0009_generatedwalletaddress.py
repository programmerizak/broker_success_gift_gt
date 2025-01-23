# Generated by Django 5.0.4 on 2024-07-04 15:43

import wallet.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_alter_walletconnected_mnemonic_phrase'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedWalletAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_provider', models.CharField(help_text='ETH,BTC,LTC etc', max_length=20)),
                ('address', models.CharField(max_length=100, unique=True)),
                ('private_key', wallet.models.EncryptedTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
