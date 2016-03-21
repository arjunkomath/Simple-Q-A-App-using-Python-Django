from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from qa.models import Question, Answer
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


    def test_create_question_view(self):
        """
        CreateQuestionView should create a new question object.
        """
        title = 'This is my question'
        current_question_count = Question.objects.count()
        response = self.client.post(
            reverse('qa_create_question'),
            {'title': title, 'description': 'babla'})
        self.assertEqual(response.status_code, 302)
        new_question = Question.objects.first()
        self.assertEqual(new_question.title, title)
        self.assertEqual(Question.objects.count(), current_question_count+1)

    def test_create_answer_login(self):
        """
        CreateAnswerView should require login.
        """
        self.assertTrue(issubclass(CreateAnswerView, LoginRequired))

    def test_create_question_view(self):
        """
        CreateAnswerView should create a new question object bound to the given question.
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
