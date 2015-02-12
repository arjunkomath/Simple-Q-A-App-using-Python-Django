# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0017_question_user_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='QVoter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.ForeignKey(to='qa.Question')),
                ('user', models.ForeignKey(to='qa.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
