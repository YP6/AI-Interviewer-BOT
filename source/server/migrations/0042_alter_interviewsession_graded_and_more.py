# Generated by Django 4.1.4 on 2023-04-19 23:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0041_alter_interviewsession_grade_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="interviewsession",
            name="graded",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="privateinterviewsusers",
            name="expiryDate",
            field=models.DateField(
                default=datetime.datetime(2023, 4, 27, 1, 58, 4, 573171)
            ),
        ),
        migrations.AlterField(
            model_name="yp6authenticationtoken",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 27, 1, 58, 4, 571174)
            ),
        ),
    ]
