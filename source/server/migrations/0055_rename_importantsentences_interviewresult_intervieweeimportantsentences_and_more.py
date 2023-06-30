# Generated by Django 4.1.4 on 2023-04-28 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0054_alter_privateinterviewsusers_expirydate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interviewresult',
            old_name='importantSentences',
            new_name='intervieweeImportantSentences',
        ),
        migrations.RenameField(
            model_name='interviewresult',
            old_name='importantWords',
            new_name='intervieweeImportantWords',
        ),
        migrations.AddField(
            model_name='interviewresult',
            name='rightAnswer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='interviewresult',
            name='rightImportantSentences',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='interviewresult',
            name='rightImportantWords',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='privateinterviewsusers',
            name='expiryDate',
            field=models.DateField(default=datetime.datetime(2023, 5, 5, 14, 3, 25, 469544)),
        ),
        migrations.AlterField(
            model_name='yp6authenticationtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 5, 14, 3, 25, 467517)),
        ),
    ]