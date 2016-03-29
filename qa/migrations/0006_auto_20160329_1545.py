# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_auto_20160329_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='answervote',
            name='value',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='questionvote',
            name='value',
            field=models.BooleanField(default=True),
        ),
    ]
