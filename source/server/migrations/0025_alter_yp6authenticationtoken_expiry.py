# Generated by Django 4.1.4 on 2023-03-27 14:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0024_alter_yp6authenticationtoken_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="yp6authenticationtoken",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 3, 16, 49, 55, 680853)
            ),
        ),
    ]
