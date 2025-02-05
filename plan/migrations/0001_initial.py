# Generated by Django 5.0.4 on 2025-01-11 06:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100, unique=True)),
                ('minimum', models.DecimalField(decimal_places=2, max_digits=12)),
                ('maximum', models.DecimalField(decimal_places=2, max_digits=12)),
                ('duration', models.PositiveIntegerField(help_text='Duration in days ')),
                ('roi', models.DecimalField(decimal_places=2, help_text='ROI Percentage', max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_invested', models.DecimalField(decimal_places=2, max_digits=12)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], default='active', max_length=20)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans_user', to='plan.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
