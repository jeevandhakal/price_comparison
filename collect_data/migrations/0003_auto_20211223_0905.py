# Generated by Django 3.2.9 on 2021-12-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect_data', '0002_auto_20211212_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='available_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='wanted_price',
            field=models.IntegerField(default=0),
        ),
    ]