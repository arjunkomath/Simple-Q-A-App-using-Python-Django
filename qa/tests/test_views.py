from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


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

    def test_login_required(self):
        """
        If user is anonymous, this page should
        redirect to the login page
        """
        client = Client()
        response = client.get(reverse('qa_create_question'))
        response_url = response.url.split('?')[0]
        self.assertEqual(response_url, 'http://testserver' + settings.LOGIN_URL)
