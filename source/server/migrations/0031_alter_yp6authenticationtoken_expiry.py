# Generated by Django 4.1.4 on 2023-03-31 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0030_alter_yp6authenticationtoken_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="yp6authenticationtoken",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 7, 13, 28, 4, 674420)
            ),
        ),
    ]
