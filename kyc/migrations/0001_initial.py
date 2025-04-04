# Generated by Django 5.0.4 on 2025-01-23 05:34

import django.core.validators
import django.db.models.deletion
import easy_thumbnails.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kyc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email_address', models.EmailField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 14 digits allowed .", regex='^\\+?1?\\d{9,14}$')])),
                ('address_line_1', models.CharField(max_length=200)),
                ('address_line_2', models.CharField(blank=True, help_text='Optional', max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('nationality', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=20)),
                ('ID_front', easy_thumbnails.fields.ThumbnailerImageField(upload_to='kyc/id_front')),
                ('ID_back', easy_thumbnails.fields.ThumbnailerImageField(upload_to='kyc/id_back')),
                ('verify_status', models.CharField(choices=[('unverified', 'unverified'), ('verified', 'verified')], default='unverified', max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_kyc', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
