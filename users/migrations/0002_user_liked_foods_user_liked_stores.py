# Generated by Django 5.0 on 2023-12-24 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_initial'),
        ('stores', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_foods',
            field=models.ManyToManyField(to='foods.food'),
        ),
        migrations.AddField(
            model_name='user',
            name='liked_stores',
            field=models.ManyToManyField(to='stores.store'),
        ),
    ]
