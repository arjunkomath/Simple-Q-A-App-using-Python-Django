import pytz
from datetime import datetime
from django.utils import timezone
from math import log

# uses a version of reddit score algorithm
# https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9#.aef67efq1


def question_score(question):
    creation_date = question.pub_date
    score = question.total_points
    answers_positive_points = list(
        question.answer_set.all().values_list(
            'answervote__value', flat=True)).count(True)
    answers_negative_points = list(
        question.answer_set.all().values_list(
            'answervote__value', flat=True)).count(False)
    score = score * 2 + answers_positive_points - answers_negative_points
    reference_date = pytz.timezone(
        timezone.get_default_timezone_name()).localize(datetime(1970, 1, 1))
    difference = creation_date - reference_date
    difference_seconds = difference.days * 86400 + difference.seconds +\
        (float(difference.microseconds) / 1000000)
    order = log(max(abs(score), 1), 10)
    sign = 1 if score > 0 else -1 if score < 0 else 0
    seconds = difference_seconds - 1134028003
    return round(sign * order + seconds / 45000, 7)
