# Generated by Django 5.0 on 2023-12-24 15:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image_url', models.TextField()),
                ('phone', models.TextField()),
                ('address', models.TextField()),
                ('email', models.TextField()),
                ('license_image_url', models.TextField()),
                ('owner_name', models.TextField()),
                ('note', models.TextField()),
                ('deny_reason', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')], max_length=8)),
            ],
        ),
    ]
