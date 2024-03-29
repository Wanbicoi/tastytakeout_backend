# Generated by Django 5.0 on 2024-01-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_alter_store_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='deny_reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='email',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='image_url',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='license_image_url',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='note',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='owner_name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='phone',
            field=models.TextField(null=True),
        ),
    ]
