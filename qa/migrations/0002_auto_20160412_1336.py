# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='votes',
        ),
    ]
