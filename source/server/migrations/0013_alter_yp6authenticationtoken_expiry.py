# Generated by Django 4.1.4 on 2023-02-02 18:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0012_alter_yp6authenticationtoken_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="yp6authenticationtoken",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 9, 20, 26, 55, 221429)
            ),
        ),
    ]
