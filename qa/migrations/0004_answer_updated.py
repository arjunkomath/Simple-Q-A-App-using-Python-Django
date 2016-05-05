# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20160414_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 5, 16, 11, 48, 760837, tzinfo=utc), verbose_name=b'date updated', auto_now=True),
            preserve_default=False,
        ),
    ]
