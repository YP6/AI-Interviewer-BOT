# Generated by Django 4.1.4 on 2023-02-05 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0017_alter_user_dateofbirth_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lastName',
        ),
        migrations.AlterField(
            model_name='yp6authenticationtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 12, 18, 21, 11, 30173)),
        ),
    ]
