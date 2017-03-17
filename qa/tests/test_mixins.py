from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.views.generic import DetailView, View

from ..mixins import AuthorRequiredMixin, LoginRequired
from ..models import Question


class SomeView(LoginRequired, View):

    def get(self, request):
        return HttpResponse('something')


class SomeAuthorRequiredView(AuthorRequiredMixin, DetailView):

    model = Question

    def get(self, request, pk):
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

    def test_author_required_allow_object_user(self):
        """
        The owner of the object should be able to access
        the view
        """
        request = self.factory.get('some-random-place')
        request.user = get_user_model().objects.create_user(
            username='test_user',
            password='top_secret'
        )
        question = Question.objects.create(
            title="Another Question",
            description="A not so long random text to fill this field",
            pub_date=timezone.datetime(2016, 1, 6, 0, 0, 0),
            reward=0,
            user=request.user,
            closed=False,
        )
        response = SomeAuthorRequiredView.as_view()(request, pk=question.pk)
        self.assertEqual(response.status_code, 200)

    def test_author_required_not_allow_not_object_user(self):
        """
        A different user than the object's owner should not
        be able to access the view, a PermissionDenied should
        be raised
        """
        request = self.factory.get('some-random-place')
        request.user = AnonymousUser()
        user = get_user_model().objects.create_user(
            username='test_user',
            password='top_secret'
        )
        question = Question.objects.create(
            title="Another Question",
            description="A not so long random text to fill this field",
            pub_date=timezone.datetime(2016, 1, 6, 0, 0, 0),
            reward=0,
            user=user,
            closed=False,
        )
        with self.assertRaises(PermissionDenied):
            SomeAuthorRequiredView.as_view()(
                request, pk=question.pk)
