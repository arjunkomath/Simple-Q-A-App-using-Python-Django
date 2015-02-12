from django.db import models

class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('slug',)

from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='qa/static/profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

from django_markdown.models import MarkdownField

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tags = models.ManyToManyField(Tag)
    reward = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user_data = models.ForeignKey(UserProfile)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = MarkdownField()
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    user_data = models.ForeignKey(UserProfile)
    def __str__(self):
        return self.answer_text

class Voter(models.Model):
    user = models.ForeignKey(UserProfile)
    answer = models.ForeignKey(Answer)

class QVoter(models.Model):
    user = models.ForeignKey(UserProfile)
    question = models.ForeignKey(Question)

class Comment(models.Model):
    answer = models.ForeignKey(Answer)
    comment_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user_data = models.ForeignKey(UserProfile)
    def __str__(self):
        return self.comment_text
