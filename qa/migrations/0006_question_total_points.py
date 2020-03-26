# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_auto_20160519_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
    ]
