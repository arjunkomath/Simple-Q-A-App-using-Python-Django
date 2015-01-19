# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_auto_20150119_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 11, 57, 14, 994152), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]
