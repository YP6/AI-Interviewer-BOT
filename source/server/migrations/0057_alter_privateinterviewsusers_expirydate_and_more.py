# Generated by Django 4.1.4 on 2023-04-28 21:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0056_remove_question_level_question_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privateinterviewsusers',
            name='expiryDate',
            field=models.DateField(default=datetime.datetime(2023, 5, 6, 0, 1, 20, 641845)),
        ),
        migrations.AlterField(
            model_name='yp6authenticationtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 6, 0, 1, 20, 639433)),
        ),
    ]