from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from qa.models import Question


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
