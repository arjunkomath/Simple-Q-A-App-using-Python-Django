# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0018_qvoter'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
