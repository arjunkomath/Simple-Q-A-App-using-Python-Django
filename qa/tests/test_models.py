from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

from qa.models import (Question, Answer, AnswerComment, QuestionComment,
                       QuestionVote, AnswerVote, UserQAProfile)


class BasicTaggingTest(object):
    """Defining a basic testcase method to be able to validate the tags on each
    model record, this is needed because the way django-taggit works.

    Disclaimer:
    Taken without remorse from:
    https://github.com/alex/django-taggit/blob/develop/tests/tests.py
    """
    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
        got = [getattr(obj, attr) for obj in qs]
        if sort:
            got.sort()
            tags.sort()
        self.assertEqual(got, tags)


class TestModels(TestCase, BasicTaggingTest):
    """TestCase class to test the models functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@swapps.co',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create_user(
            username='other_test_user',
            email='other_test@swapps.co',
            password='top_secret'
        )
        self.first_question = Question.objects.create(
            title="Another Question",
            description="A not so long random text to fill this field",
            pub_date=timezone.datetime(2016, 1, 6, 0, 0, 0),
            reward=0,
            user=self.user,
            closed=False,
        )
        self.first_answer = Answer.objects.create(
            question=self.first_question,
            answer_text="I hope this text is acceptable by django_markdown",
            pub_date=timezone.datetime(2016, 2, 6, 0, 0, 0),
            user=self.user,
        )

    def test_question(self):
        self.first_question.tags.add('one tag', 'the next tag', 'another tag')
        self.assertEqual(self.first_question.title, "Another Question")
        self.assertTrue(isinstance(self.first_question, Question))
        self.assertNotEqual(self.first_question.pub_date, timezone.now())
        self.assert_tags_equal(self.first_question.tags.all(),
                               ['one tag', 'the next tag', 'another tag'])

    def test_answer(self):
        answer = Answer.objects.create(
            question=self.first_question,
            answer_text="A text body",
            pub_date=timezone.datetime(2016, 2, 7, 0, 0, 0),
            user=self.user,
        )
        self.assertTrue(isinstance(answer, Answer))
        self.assertTrue(isinstance(self.first_answer, Answer))
        self.assertEqual(self.first_answer.answer_text,
                         "I hope this text is acceptable by django_markdown")
        self.assertEqual(answer.answer_text, "A text body")

    def test_answer_comment(self):
        comment = AnswerComment.objects.create(
            answer=self.first_answer,
            comment_text="This is not so bright a comment",
            pub_date=timezone.datetime(2016, 2, 8, 0, 0, 0),
            user=self.user)
        self.assertTrue(isinstance(comment, AnswerComment))

    def test_question_comment(self):
        comment = QuestionComment.objects.create(
            question=self.first_question,
            comment_text="This is not so bright a comment",
            pub_date=timezone.datetime(2016, 2, 8, 0, 0, 0),
            user=self.user)
        self.assertTrue(isinstance(comment, QuestionComment))

    def test_question_vote(self):
        vote = QuestionVote.objects.create(user=self.user,
                                           value=True,
                                           question=self.first_question)
        self.assertTrue(isinstance(vote, QuestionVote))

    def test_answer_vote(self):
        vote = AnswerVote.objects.create(user=self.user,
                                         value=True,
                                         answer=self.first_answer)
        self.assertTrue(isinstance(vote, AnswerVote))

    def test_autogenerate_slug(self):
        """Test that creates a slug when question saves"""
        self.assertEqual(
            self.first_question.slug, slugify(self.first_question.slug))

    def test_user_creation(self):
        qa_user = UserQAProfile.objects.get(user=self.user)
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(qa_user.user, self.user)
        self.assertEqual(qa_user.user.username, 'test_user')
        self.assertTrue(isinstance(qa_user, UserQAProfile))
        self.assertTrue(isinstance(other_qa_user, UserQAProfile))

    def test_reputation_modification(self):
        qa_user = UserQAProfile.objects.get(user=self.user)
        self.assertEqual(qa_user.points, 0)
        qa_user.modify_reputation(3)
        qa_user.refresh_from_db()
        self.assertEqual(qa_user.points, 3)
        qa_user.modify_reputation(1)
        qa_user.refresh_from_db()
        self.assertEqual(qa_user.points, 4)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_QUESTION': 4}})
    def test_affect_reputation_by_question(self):
        """
        This test validates than the UserQAProfile method modify_reputation
        works properly when a Question instance is created.
        """
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(other_qa_user.points, 0)
        question = Question.objects.create(
            title="Additional Question",
            description="A not so long random text",
            pub_date=timezone.datetime(2016, 1, 6, 0, 0, 0),
            reward=0,
            user=self.other_user,
            closed=False,)
        self.assertTrue(isinstance(question, Question))
        other_qa_user.refresh_from_db()
        self.assertEqual(other_qa_user.points, 4)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_ANSWER': 4}})
    def test_affect_reputation_by_answer(self):
        """
        This test validates than the UserQAProfile method modify_reputation
        works properly when an Answer instance is created
        """
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(other_qa_user.points, 0)
        answer = Answer.objects.create(
            question=self.first_question,
            answer_text="A text body",
            pub_date=timezone.datetime(2016, 2, 7, 0, 0, 0),
            user=self.other_user,
        )
        self.assertTrue(isinstance(answer, Answer))
        other_qa_user.refresh_from_db()
        self.assertEqual(other_qa_user.points, 4)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_ANSWER_COMMENT': 4}})
    def test_affect_reputation_by_answercomment(self):
        """
        This test validates than the UserQAProfile method modify_reputation
        works properly when an AnswerComment instance is created
        """
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(other_qa_user.points, 0)
        comment = AnswerComment.objects.create(
            answer=self.first_answer,
            comment_text="This is not so bright a comment",
            pub_date=timezone.datetime(2016, 2, 8, 0, 0, 0),
            user=self.other_user)
        self.assertTrue(isinstance(comment, AnswerComment))
        other_qa_user.refresh_from_db()
        self.assertEqual(other_qa_user.points, 4)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_QUESTION_COMMENT': 4}})
    def test_affect_reputation_by_questioncomment(self):
        """
        This test validates than the UserQAProfile method modify_reputation
        works properly when an QuestionComment instance is created
        """
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(other_qa_user.points, 0)
        comment = QuestionComment.objects.create(
            question=self.first_question,
            comment_text="This is not so bright a comment",
            pub_date=timezone.datetime(2016, 2, 8, 0, 0, 0),
            user=self.other_user)
        self.assertTrue(isinstance(comment, QuestionComment))
        other_qa_user.refresh_from_db()
        self.assertEqual(other_qa_user.points, 4)

    @override_settings(QA_SETTINGS={})
    def test_affect_reputation_by_answercomment(self):
        """
        This test validates than the UserQAProfile method modify_reputation
        works properly when an AnswerComment instance is created, but
        there is no QA_SETTING defined inside the settings file, so the
        try block inside the save() method of the model goes for the
        excep line.
        """
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(other_qa_user.points, 0)
        comment = AnswerComment.objects.create(
            answer=self.first_answer,
            comment_text="This is not so bright a comment",
            pub_date=timezone.datetime(2016, 2, 8, 0, 0, 0),
            user=self.other_user)
        self.assertTrue(isinstance(comment, AnswerComment))
        other_qa_user.refresh_from_db()
        self.assertEqual(other_qa_user.points, 0)

    @override_settings(QA_SETTINGS={})
    def test_affect_reputation_by_questioncomment(self):
        """
        This test validates than the UserQAProfile method modify_reputation
        works properly when an QuestionComment instance is created, but
        there is no QA_SETTING defined inside the settings file, so the
        try block inside the save() method of the model goes for the
        excep line.
        """
        other_qa_user = self.other_user.userqaprofile
        self.assertEqual(other_qa_user.points, 0)
        comment = QuestionComment.objects.create(
            question=self.first_question,
            comment_text="This is not so bright a comment",
            pub_date=timezone.datetime(2016, 2, 8, 0, 0, 0),
            user=self.other_user)
        self.assertTrue(isinstance(comment, QuestionComment))
        other_qa_user.refresh_from_db()
        self.assertEqual(other_qa_user.points, 0)
