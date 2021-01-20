# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='payment_details',
            fields=[
                ('ID', models.AutoField(primary_key=True, unique=True, serialize=False)),
                ('Credit_Card_Number', models.CharField(max_length=200)),
                ('Card_Holder', models.CharField(max_length=200)),
                ('ExpirationDate', models.DateTimeField()),
                ('SecurityCode', models.CharField(max_length=200)),
                ('Amount', models.IntegerField()),
            ],
        ),
    ]
