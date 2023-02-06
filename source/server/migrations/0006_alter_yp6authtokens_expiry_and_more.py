# Generated by Django 4.1.4 on 2023-01-29 18:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_yp6authtokens_macaddress_alter_yp6authtokens_expiry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yp6authtokens',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 5, 20, 2, 40, 348221)),
        ),
        migrations.AlterField(
            model_name='yp6authtokens',
            name='macAddress',
            field=models.TextField(default='0.0.0.0', max_length=20),
        ),
        migrations.AlterField(
            model_name='yp6authtokens',
            name='token',
            field=models.TextField(default='None', max_length=64),
        ),
    ]