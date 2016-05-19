# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_answer_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='negative_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='positive_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='negative_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='positive_votes',
            field=models.IntegerField(default=0),
        ),
    ]
