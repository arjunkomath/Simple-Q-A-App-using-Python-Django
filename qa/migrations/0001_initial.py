# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_markdown.models
from django.conf import settings
import taggit.managers
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', django_markdown.models.MarkdownField()),
                ('votes', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
                ('comment_text', django_markdown.models.MarkdownField()),
                ('answer', models.ForeignKey(to='qa.Answer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.BooleanField(default=True)),
                ('answer', models.ForeignKey(to='qa.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('description', django_markdown.models.MarkdownField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
                ('reward', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('closed', models.BooleanField(default=False)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
                ('comment_text', models.CharField(max_length=250)),
                ('question', models.ForeignKey(to='qa.Question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.BooleanField(default=True)),
                ('question', models.ForeignKey(to='qa.Question')),
            ],
        ),
        migrations.CreateModel(
            name='UserQAProfile',
            fields=[
                ('user', annoying.fields.AutoOneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('points', models.IntegerField(default=0)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'qa/static/profile_images', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='questionvote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answervote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answercomment',
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
        migrations.AlterUniqueTogether(
            name='questionvote',
            unique_together=set([('user', 'question')]),
        ),
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together=set([('user', 'answer')]),
        ),
    ]
