# Generated by Django 4.1.4 on 2023-01-29 19:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_alter_yp6authenticationtoken_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yp6authenticationtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 5, 21, 35, 26, 105487)),
        ),
    ]
