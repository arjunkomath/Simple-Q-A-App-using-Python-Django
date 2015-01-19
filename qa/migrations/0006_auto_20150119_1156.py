# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_answer_user_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='user_data',
            field=models.ForeignKey(to='qa.UserProfile'),
            preserve_default=True,
        ),
    ]
