from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from qa.models import Question


class TestModels(TestCase):
    """TestCase class to test the models functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@swapps.co',
            password='top_secret'
        )
        self.another_one = Question.objects.create(
            title="Another Question",
            description="A not so long random text to fill this field",
            pub_date=timezone.datetime(2016, 1, 6, 0, 0, 0),
            reward=0,
            views=3,
            user=self.user,
            closed=False,
        )

    def test_another_question(self):
        self.another_one.tags.add('one tag', 'the next tag', 'another tag')
        self.assertEqual(self.another_one.title, "Another Question")
        self.assertTrue(isinstance(self.another_one, Question))
        self.assertNotEqual(self.another_one.pub_date, timezone.now())
