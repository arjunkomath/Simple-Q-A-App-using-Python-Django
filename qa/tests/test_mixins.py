from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from ..mixins import LoginRequired


class SomeView(LoginRequired, View):

    def get(self, request):
        return HttpResponse('something')


class TestMixins(TestCase):
    """
    Tests functionalities for the mixins.
    Views that implement them should only test
    that they are subclasses of the given mixin.
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_login_required_redirects(self):
        """
        Anonymous users should be redirected to the LOGIN_URL
        """
        request = self.factory.get('some-random-place')
        request.user = AnonymousUser()
        response = SomeView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response.url)

    def test_login_request_access(self):
        """
        Authenticated users should be able to access the view.
        """
        request = self.factory.get('some-random-place')
        request.user = get_user_model().objects.create_user(
            username='test_user',
            password='top_secret'
        )
        response = SomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
