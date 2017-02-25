from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import (Question, Answer, AnswerComment,
                     QuestionComment, UserQAProfile)


@receiver(post_save, sender=Question)
def affect_rep_at_question_creation(sender, instance, created, **kwargs):
    if not created:
        try:
            points = settings.QA_SETTINGS['reputation']['CREATE_QUESTION']

        except KeyError:
            points = 0

        qa_user = UserQAProfile.objects.get(user_id=instance.user)
        qa_user.modify_reputation(points)


@receiver(post_save, sender=Answer)
def affect_rep_at_answer_creation(sender, instance, created, **kwargs):
    if not created:
        try:
            points = settings.QA_SETTINGS['reputation']['CREATE_ANSWER']

        except KeyError:
            points = 0

        qa_user = UserQAProfile.objects.get(user_id=instance.user)
        qa_user.modify_reputation(points)


@receiver(post_save, sender=QuestionComment)
def affect_rep_at_questioncomment_creation(sender,
                                           instance, created, **kwargs):
    if not created:
        try:
            points = settings.QA_SETTINGS[
                'reputation']['CREATE_QUESTION_COMMENT']

        except KeyError:
            points = 0

        qa_user = UserQAProfile.objects.get(user_id=instance.user)
        qa_user.modify_reputation(points)


@receiver(post_save, sender=AnswerComment)
def affect_rep_at_answercomment_creation(sender,
                                         instance, created, **kwargs):
    if not created:
        try:
            points = settings.QA_SETTINGS[
                'reputation']['CREATE_ANSWER_COMMENT']

        except KeyError:
            points = 0

        qa_user = UserQAProfile.objects.get(user_id=instance.user)
        qa_user.modify_reputation(points)
