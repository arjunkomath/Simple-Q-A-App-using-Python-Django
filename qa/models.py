from django.db import models
from django.conf import settings
from django_markdown.models import MarkdownField

from taggit.managers import TaggableManager
from annoying.fields import AutoOneToOneField


class UserQAProfile(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    points = models.IntegerField(default=0)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='qa/static/profile_images',
                                blank=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = MarkdownField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = TaggableManager()
    reward = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    closed = models.BooleanField(default=False)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_points = self.positive_votes - self.negative_votes
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = MarkdownField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    answer = models.BooleanField(default=False)
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_points = self.positive_votes - self.negative_votes
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.answer_text


class VoteParent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    value = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AnswerVote(VoteParent):
    answer = models.ForeignKey(Answer)

    class Meta:
        unique_together = (('user', 'answer'),)


class QuestionVote(VoteParent):
    question = models.ForeignKey(Question)

    class Meta:
        unique_together = (('user', 'question'),)


class BaseComment(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True

    def __str__(self):
        return self.comment_text


class AnswerComment(BaseComment):
    comment_text = MarkdownField()
    answer = models.ForeignKey(Answer)


class QuestionComment(BaseComment):
    comment_text = models.CharField(max_length=250)
    question = models.ForeignKey(Question)
