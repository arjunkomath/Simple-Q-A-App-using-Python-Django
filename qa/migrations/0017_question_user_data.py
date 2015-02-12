# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0016_question_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='user_data',
            field=models.ForeignKey(default=5, to='qa.UserProfile'),
            preserve_default=False,
        ),
    ]
