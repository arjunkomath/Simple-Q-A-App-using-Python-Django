# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncomment',
            name='comment_text',
            field=models.CharField(max_length=250),
        ),
    ]
