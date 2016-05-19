# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_question_total_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
    ]
