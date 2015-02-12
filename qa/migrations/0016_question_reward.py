# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0015_answer_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='reward',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
