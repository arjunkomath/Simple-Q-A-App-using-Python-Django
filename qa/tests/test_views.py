from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from qa.models import (Question, Answer, QuestionComment, QuestionVote,
                       AnswerVote)
from qa.mixins import LoginRequired
from qa.views import CreateQuestionView, CreateAnswerView


class TestViews(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@swapps.co',
            password='top_secret'
        )
        self.client.login(username='test_user', password='top_secret')

    def test_create_question_login(self):
        """
        CreateQuestionView should require login.
        Assertion can be made just by checking that the correct mixin
        is a superclass.
        """
        self.assertTrue(issubclass(CreateQuestionView, LoginRequired))

    def test_create_answer_login(self):
        """
        CreateAnswerView should require login.
        """
        self.assertTrue(issubclass(CreateAnswerView, LoginRequired))

    def test_create_question_view_one(self):
        """
        CreateQuestionView should create a new question object.
        """
        title = 'This is my question'
        current_question_count = Question.objects.count()
        response = self.client.post(
            reverse('qa_create_question'),
            {'title': title, 'description': 'babla', 'tags': ' '})
        self.assertEqual(response.status_code, 302)
        new_question = Question.objects.first()
        self.assertEqual(new_question.title, title)
        self.assertEqual(Question.objects.count(), current_question_count+1)

    def test_create_question_view_two(self):
        """
        CreateAnswerView should create a new question object bound to the
        given question.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        current_answer_count = Answer.objects.filter(question=question).count()
        response = self.client.post(
            reverse('qa_create_answer', kwargs={'question_id': question.pk}),
            {'question': question, 'answer_text': 'some_text_here'})
        self.assertEqual(response.status_code, 302)
        new_answer = Answer.objects.first()
        self.assertEqual(new_answer.question, question)
        self.assertEqual(Answer.objects.count(), current_answer_count+1)

# CreateQuestionCommentView

    def test_create_question_comment_view(self):
        """
        CreateQuestionCommentView should create a new question comment object
        bound to the
        given question.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        current_comment_question_count = QuestionComment.objects.filter(
            question=question).count()
        response = self.client.post(
            reverse('qa_create_question_comment',
                    kwargs={'question_id': question.pk}),
            {'comment_text': 'some_text_here'})
        self.assertEqual(response.status_code, 302)
        new_comment = QuestionComment.objects.first()
        self.assertEqual(new_comment.question, question)
        self.assertEqual(QuestionComment.objects.count(),
                         current_comment_question_count+1)

    def test_user_cannot_upvote_own_questions(self):
        """
        When some user upvotes a question, and it is his own question
        an error should be raised, because that's not allowed.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        with self.assertRaises(ValidationError):
            response = self.client.post(reverse(
                'qa_question_vote', kwargs={'object_id': question.id}),
                data={'upvote': 'on'})

    def test_can_upvote_question(self):
        """
        When i upvote a question, the question field gets updated
        and a new instance of QuestionVote is created.
        Shares same base class as answer votes.
        """
        user = get_user_model().objects.create_user(username='user2',
                                                    password='top_secret')
        question = Question.objects.create(
            title='a title', description='bla', user=user)
        previous_votes = question.total_points
        previous_vote_instances = QuestionVote.objects.count()
        response = self.client.post(reverse(
            'qa_question_vote', kwargs={'object_id': question.id}),
            data={'upvote': 'on'})
        self.assertEqual(response.status_code, 302)
        question.refresh_from_db()
        self.assertEqual(previous_votes + 1, question.total_points)
        self.assertEqual(previous_vote_instances + 1,
                         QuestionVote.objects.count())

    def test_can_downvote_answer(self):
        """
        When i downvote an answer, the answer field gets updated
        and a new instance of AnswerVote is created.
        """
        user = get_user_model().objects.create_user(username='user2',
                                                    password='top_secret')
        question = Question.objects.create(
            title='a title', description='bla', user=user)
        answer = Answer.objects.create(
            answer_text='a title', user=user, question=question)
        previous_votes = question.total_points
        previous_vote_instances = AnswerVote.objects.count()
        response = self.client.post(reverse('qa_answer_vote',
                                    kwargs={'object_id': answer.id}))
        self.assertEqual(response.status_code, 302)
        answer.refresh_from_db()
        self.assertEqual(previous_votes - 1, answer.total_points)
        self.assertEqual(previous_vote_instances + 1,
                         AnswerVote.objects.count())

    def test_upvote_question_deletes_instance(self):
        """
        When a user upvotes a question that was already upvoted, the vote
        is reverted. This means that the vote count goes down and the
        vote instance is removed.
        """
        user = get_user_model().objects.create_user(username='user2',
                                                    password='top_secret')
        question = Question.objects.create(
            title='a title', description='bla', user=user)
        QuestionVote.objects.create(user=self.user, question=question,
                                    value=True)
        previous_vote_instances = QuestionVote.objects.count()
        previous_votes = question.total_points
        response = self.client.post(reverse('qa_question_vote',
                                    kwargs={'object_id': question.id}),
                                    data={'upvote': 'on'})
        self.assertEqual(previous_vote_instances - 1,
                         QuestionVote.objects.count())
        question.refresh_from_db()
        self.assertEqual(previous_votes - 1, question.total_points)

    def test_switching_vote_updates_correctly(self):
        """
        If i downvote an already upvoted question, the count should
        shift downwards by 2 because i am not only retiring my upvote, I am
        adding a negative vote too. The vote instance should be updated too.
        """
        user = get_user_model().objects.create_user(username='user2',
                                                    password='top_secret')
        question = Question.objects.create(
            title='a title', description='bla', user=user)
        question_vote = QuestionVote.objects.create(user=self.user,
                                                    question=question,
                                                    value=True)
        previous_vote_instances = QuestionVote.objects.count()
        previous_votes = question.total_points
        previous_question_vote = question_vote.value
        response = self.client.post(reverse('qa_question_vote',
                                    kwargs={'object_id': question.id}))
        self.assertEqual(previous_vote_instances, QuestionVote.objects.count())
        question.refresh_from_db()
        question_vote.refresh_from_db()
        self.assertEqual(previous_votes - 2, question.total_points)
        self.assertNotEqual(previous_question_vote, question_vote.value)
