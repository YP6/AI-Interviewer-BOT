# Generated by Django 4.1.4 on 2023-02-05 17:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0019_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yp6authenticationtoken',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 12, 19, 35, 14, 595815)),
        ),
    ]