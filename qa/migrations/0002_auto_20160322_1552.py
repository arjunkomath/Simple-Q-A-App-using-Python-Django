# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Voter',
            new_name='AnswerVote',
        ),
        migrations.RenameModel(
            old_name='QVoter',
            new_name='QuestionVote',
        ),
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together=set([('user', 'answer')]),
        ),
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together=set([('user', 'question')]),
        ),
    ]
