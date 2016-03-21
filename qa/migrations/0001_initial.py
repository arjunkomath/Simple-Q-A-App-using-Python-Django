# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import django_markdown.models
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('answer_text', django_markdown.models.MarkdownField()),
                ('votes', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('comment_text', django_markdown.models.MarkdownField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('answer', models.ForeignKey(to='qa.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', django_markdown.models.MarkdownField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('reward', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('closed', models.BooleanField(default=False)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='QVoter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('question', models.ForeignKey(to='qa.Question')),
            ],
        ),
        migrations.CreateModel(
            name='UserQAProfile',
            fields=[
                ('user', annoying.fields.AutoOneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('points', models.IntegerField(default=0)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to='qa/static/profile_images', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('answer', models.ForeignKey(to='qa.Answer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='qvoter',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='qa.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
