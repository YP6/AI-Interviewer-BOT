# Generated by Django 4.1.4 on 2023-03-31 03:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0027_remove_interviewsession_answer_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="interviewattendance",
            name="reportID",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="server.report",
            ),
        ),
        migrations.AlterField(
            model_name="yp6authenticationtoken",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 7, 5, 14, 20, 614405)
            ),
        ),
    ]
