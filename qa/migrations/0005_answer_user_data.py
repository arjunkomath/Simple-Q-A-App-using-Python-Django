# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user_data',
            field=models.OneToOneField(default=1, to='qa.UserProfile'),
            preserve_default=False,
        ),
    ]
