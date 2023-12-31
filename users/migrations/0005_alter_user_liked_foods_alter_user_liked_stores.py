# Generated by Django 5.0 on 2023-12-28 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_alter_foodcomment_commenter'),
        ('stores', '0003_alter_store_status'),
        ('users', '0004_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_foods',
            field=models.ManyToManyField(related_name='likers', to='foods.food'),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_stores',
            field=models.ManyToManyField(related_name='likers', to='stores.store'),
        ),
    ]
