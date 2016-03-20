from django.db import models
from django.conf import settings
from django_markdown.models import MarkdownField
from django.template.defaultfilters import slugify

from annoying.fields import AutoOneToOneField


class Tag(models.Model):
    to_slug = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.q)

        super(Tag, self).save(*args, **kwargs)

    class Meta:
        ordering = ('slug',)


class UserQAProfile(models.Model):
    # This line is required. Links UserQAProfile to a User model instance.
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    points = models.IntegerField(default=0)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='qa/static/profile_images',
                                blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = MarkdownField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    reward = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = MarkdownField()
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.answer_text


class Voter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    answer = models.ForeignKey(Answer)


class QVoter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.ForeignKey(Question)


class Comment(models.Model):
    answer = models.ForeignKey(Answer)
    comment_text = MarkdownField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.comment_text
