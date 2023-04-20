# Generated by Django 4.1.4 on 2023-04-19 23:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0040_interviewsession_grade_interviewsession_graded_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="interviewsession",
            name="grade",
            field=models.FloatField(default=False),
        ),
        migrations.AlterField(
            model_name="interviewsession",
            name="processed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="interviewsession",
            name="videoPath",
            field=models.TextField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="privateinterviewsusers",
            name="expiryDate",
            field=models.DateField(
                default=datetime.datetime(2023, 4, 27, 1, 54, 45, 975302)
            ),
        ),
        migrations.AlterField(
            model_name="yp6authenticationtoken",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 27, 1, 54, 45, 974303)
            ),
        ),
    ]