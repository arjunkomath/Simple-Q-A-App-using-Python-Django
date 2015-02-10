# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0012_auto_20150120_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=b'static/profile_images', blank=True),
            preserve_default=True,
        ),
    ]
