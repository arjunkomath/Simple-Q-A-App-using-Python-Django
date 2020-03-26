from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import Client, TestCase, override_settings
from qa.mixins import LoginRequired
from qa.models import (Answer, AnswerVote, Question, QuestionComment,
                       QuestionVote, UserQAProfile, AnswerComment)
from qa.views import CreateAnswerView, CreateQuestionView


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
        self.user_two = get_user_model().objects.create_user(
            username='user2', password='top_secret')

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

    def test_profile_view(self):
        """Test than the profile view is working properly
        """
        response = self.client.get(
            reverse('qa_profile',
                    kwargs={'user_id': self.user.userqaprofile.user_id}))
        self.assertEqual(response.status_code, 200)

    def test_create_question_view_one(self):
        """
        CreateQuestionView should create a new question object.
        """
        title = 'This is my question'
        current_question_count = Question.objects.count()
        response = self.client.post(
            reverse('qa_create_question'),
            {'title': title, 'description': 'babla', 'tags': 'test tag'})
        self.assertEqual(response.status_code, 302)
        new_question = Question.objects.first()
        self.assertEqual(new_question.title, title)
        self.assertEqual(Question.objects.count(),
                         current_question_count + 1)

    @override_settings(QA_SETTINGS={'qa_description_optional': True})
    def test_create_question_optional_description(self):
        """
        When QA_DESCRIPTION_OPTIONAL is True, the validation for description
        should be disabled on the form, allowing the object to be created
        without specifying it.
        """
        title = 'This is my question'
        current_question_count = Question.objects.count()
        response = self.client.post(
            reverse('qa_create_question'),
            {'title': title, 'tags': 'test tag'})
        self.assertEqual(response.status_code, 302)
        new_question = Question.objects.last()
        self.assertEqual(new_question.title, title)
        self.assertEqual(Question.objects.count(), current_question_count + 1)

    @override_settings(QA_SETTINGS={'qa_description_optional': False})
    def test_create_question_optional_description_false(self):
        """
        When QA_DESCRIPTION_OPTIONAL is False (default), the validation for
        description will be on place, and a question cannot be created without
        setting some content for it.
        """
        title = 'This is my question'
        current_question_count = Question.objects.count()
        response = self.client.post(
            reverse('qa_create_question'),
            {'title': title, 'tags': 'test tag'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), current_question_count)

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
        self.assertEqual(
            Answer.objects.count(), current_answer_count + 1)

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
                         current_comment_question_count + 1)

    def test_updates_question_comments(self):
        """
        If an url is provided at the post request, the view should
        redirect there.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        response_q = self.client.post(
            reverse('qa_create_question_comment',
                    kwargs={'question_id': question.pk}),
            {'comment_text': 'some_text_here'})
        comment = QuestionComment.objects.latest('pub_date')
        comment_text = comment.comment_text
        response_two = self.client.post(
            reverse('qa_update_question_comment',
                    kwargs={'comment_id': comment.id}),
            {'comment_text': 'some_different_text_here'})
        comment.refresh_from_db()
        self.assertEqual(response_q.status_code, 302)
        self.assertEqual(response_two.status_code, 302)
        self.assertNotEqual(comment_text, comment.comment_text)

    def test_updates_answer_comments(self):
        """
        If an url is provided at the post request, the view should
        redirect there.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user, question=question)
        response_a = self.client.post(
            reverse('qa_create_answer_comment',
                    kwargs={'answer_id': answer.id}),
            {'comment_text': 'a description'})
        comment = AnswerComment.objects.latest('pub_date')
        comment_text = comment.comment_text
        response_two = self.client.post(
            reverse('qa_update_answer_comment',
                    kwargs={'comment_id': comment.id}),
            {'comment_text': 'some_different_text_here'})
        comment.refresh_from_db()
        self.assertEqual(response_a.status_code, 302)
        self.assertEqual(response_two.status_code, 302)
        self.assertNotEqual(comment_text, comment.comment_text)

    def test_user_cannot_upvote_own_questions(self):
        """
        When some user upvotes a question, and it is his own question
        an error should be raised, because that's not allowed.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        with self.assertRaises(ValidationError):
            self.client.post(reverse(
                'qa_question_vote', kwargs={'object_id': question.id}),
                data={'upvote': 'on'})

    def test_can_upvote_question(self):
        """
        When i upvote a question, the question field gets updated
        and a new instance of QuestionVote is created.
        Shares same base class as answer votes.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
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
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user_two, question=question)
        previous_votes = question.total_points
        previous_vote_instances = AnswerVote.objects.count()
        response = self.client.post(reverse('qa_answer_vote',
                                    kwargs={'object_id': answer.id}))
        self.assertEqual(response.status_code, 302)
        answer.refresh_from_db()
        self.assertEqual(previous_votes - 1, answer.total_points)
        self.assertEqual(answer.negative_votes, 1)
        self.assertEqual(previous_vote_instances + 1,
                         AnswerVote.objects.count())

    def test_upvote_question_deletes_instance(self):
        """
        When a user upvotes a question that was already upvoted, the vote
        is reverted. This means that the vote count goes down and the
        vote instance is removed.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        QuestionVote.objects.create(user=self.user, question=question,
                                    value=True)
        previous_vote_instances = QuestionVote.objects.count()
        previous_votes = question.total_points
        self.client.post(reverse('qa_question_vote',
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
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        question_vote = QuestionVote.objects.create(user=self.user,
                                                    question=question,
                                                    value=True)
        previous_vote_instances = QuestionVote.objects.count()
        previous_votes = question.total_points
        previous_question_vote = question_vote.value
        self.client.post(reverse('qa_question_vote',
                         kwargs={'object_id': question.id}))
        self.assertEqual(previous_vote_instances, QuestionVote.objects.count())
        question.refresh_from_db()
        question_vote.refresh_from_db()
        self.assertEqual(previous_votes - 2, question.total_points)
        self.assertNotEqual(previous_question_vote, question_vote.value)

# AnswerQuestionView

    def test_can_mark_answer_as_satisfying_answer(self):
        """
        The owner of the question should be able to mark an answer
        as the satisfying one. The question should be kept open
        """

        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user_two, question=question)
        response = self.client.post(reverse('qa_answer_question',
                                    kwargs={'answer_id': answer.id}))
        answer.refresh_from_db()
        question.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(question.closed)
        self.assertTrue(answer.answer)

    def test_can_provide_next_url_when_marking_satisfying_answer(self):
        """
        If an url is provided at the post request, the view should
        redirect there.
        """

        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user_two, question=question)
        response = self.client.post(
            reverse('qa_answer_question',
                    kwargs={'answer_id': answer.id}),
            data={'next': reverse('qa_create_question')})
        answer.refresh_from_db()
        question.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qa_create_question'))

    def test_not_owner_cannot__mark_answer_as_satisfying_answer(self):
        """
        Any user that is not the owner of the question should not be able
        to mark an user as the satisfying one.
        """

        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user, question=question)
        with self.assertRaises(ValidationError):
            self.client.post(reverse('qa_answer_question',
                             kwargs={'answer_id': answer.id}))
            answer.refresh_from_db()
            self.assertFalse(answer.answer)

# CloseQuestionView

    def test_can_mark_close_question(self):
        """
        The owner of the question should be able to
        close it
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        response = self.client.post(reverse('qa_close_question',
                                    kwargs={'question_id': question.id}))
        question.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(question.closed)

    def test_can_not_mark_closed_question(self):
        """
        The question is already closed, so the view should rises a
        ValidationError
        """
        question = Question.objects.create(title='a title', description='bla',
                                           closed=True, user=self.user)
        with self.assertRaises(ValidationError):
            response = self.client.post(
                reverse('qa_close_question',
                        kwargs={'question_id': question.id}))
            self.assertEqual(response.status_code, 302)

        self.assertTrue(question.closed)

    def test_can_provide_next_url_when_closing_question(self):
        """
        If an url is provided at the post request, the view should
        redirect there.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        response = self.client.post(
            reverse('qa_close_question',
                    kwargs={'question_id': question.id}),
            data={'next': reverse('qa_create_question')})
        question.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qa_create_question'))

    def test_not_owner_cannot_close_question(self):
        """
        Any user that is not the owner of the question should not be able
        to close question.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        with self.assertRaises(ValidationError):
            self.client.post(reverse('qa_close_question',
                             kwargs={'question_id': question.id}))
            self.assertFalse(question.closed)

# QuestionIndexView

    def test_question_index_returns_all_questions(self):
        """
        QuestionIndexView should return all questions,
        questions with no answers and the questions with
        points
        """
        title = 'This is my question'
        self.client.post(
            reverse('qa_create_question'),
            {'title': title, 'description': 'babla', 'tags': 'test tag'})
        response = self.client.get(reverse('qa_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['questions']),
            list(Question.objects.all()))
        self.assertEqual(
            list(response.context['noans']),
            list(Question.objects.all()))
        self.assertEqual(
            list(response.context['reward']), [])

    def test_question_search_returns_related_questions(self):
        """
        QuestionsSearchView should return questions
        containing the search term
        """
        self.client.post(
            reverse('qa_create_question'),
            {'title': "first title",
             'description': 'first description',
             'tags': 'test tag'})
        self.client.post(
            reverse('qa_create_question'),
            {'title': "second title",
             'description': 'second description',
             'tags': 'test tag'})
        response = self.client.get(reverse('qa_search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['questions']),
            len(Question.objects.all()))
        self.assertEqual(
            len(response.context['noans']),
            len(Question.objects.all()))
        self.assertEqual(
            len(response.context['reward']), 0)
        response = self.client.get(
            reverse('qa_search'), data={'word': 'first'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['questions']),
            len(Question.objects.filter(title="first title")))
        response = self.client.get(
            reverse('qa_search'), data={'word': 'second'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['questions']),
            len(Question.objects.filter(title="second title")))

# QuestionsByTagView

    def test_question_by_tag_returns_related_tag_questions(self):
        """
        QuestionsByTagView should return questions related
        with searched tag
        """
        self.client.post(reverse('qa_create_question'),
                         {'title': "first title",
                          'description': 'first description',
                          'tags': 'tag'})
        self.client.post(reverse('qa_create_question'),
                         {'title': "second title",
                          'description': 'second description',
                          'tags': 'test'})
        response = self.client.get(reverse('qa_tag', kwargs={'tag': 'tag'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['questions']),
                         len(Question.objects.filter(title="first title")))
        response = self.client.get(reverse('qa_tag', kwargs={'tag': 'test'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['questions']),
                         len(Question.objects.filter(title="second title")))

# UpdateQuestionView

    def test_updates_question_modify_question(self):
        """
        UpdateQuestionView updates the required question
        """
        self.client.post(
            reverse('qa_create_question'), {'title': "first title",
                                            'description': 'first description',
                                            'tags': 'tag'})
        question = Question.objects.latest('pub_date')
        question_title = question.title
        question_description = question.description
        response = self.client.post(
            reverse('qa_update_question',
                    kwargs={'question_id': question.id}),
            {'title': "second title",
             'description': 'second description',
             'tags': 'test'})
        question.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(question_title, question.title)
        self.assertNotEqual(question_description, question.description)


# UpdateAnswerView

    def test_updates_answer_modify_answer(self):
        """
        UpdateQuestionView updates the required answer
        """

        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user, question=question)
        answer_text = answer.answer_text
        response = self.client.post(
            reverse('qa_update_answer',
                    kwargs={'answer_id': answer.id}),
            {'answer_text': 'a description'})
        answer.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(answer_text, answer.answer_text)

# CreateAnswerCommentView

    def test_create_answer_comment_create_comment_to_given_answer(self):
        """
        CreateAnswerCommentView creates comment to given answer
        """

        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user, question=question)
        answer_comments = len(answer.answercomment_set.all())
        response = self.client.post(
            reverse('qa_create_answer_comment',
                    kwargs={'answer_id': answer.id}),
            {'comment_text': 'a description'})
        answer.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(
            answer_comments, answer.answercomment_set.all())

# Test reputation

    @override_settings(QA_SETTINGS={'reputation': {'ACCEPT_ANSWER': 4}})
    def test_affect_reputation_when_providing_the_answer_of_choice(self):
        """
        This test validates than the view alters properly the right QA user
        profile when it updates the reputation points at the moment of
        an answer acceptance.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user_two, question=question)
        qa_user = UserQAProfile.objects.get(user_id=self.user)
        qa_user_two = UserQAProfile.objects.get(user_id=self.user_two)
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        response = self.client.post(reverse('qa_answer_question',
                                    kwargs={'answer_id': answer.id}))
        qa_user.refresh_from_db()
        qa_user_two.refresh_from_db()
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 4)
        self.assertEqual(response.status_code, 302)

    @override_settings(QA_SETTINGS={})
    def test_affect_reputation_when_providing_the_answer_of_choice_without(self):
        """
        This test validates than the view alters properly the right QA user
        profile when it updates the reputation points at the moment of
        an answer acceptance in case the QA_SETTINGS variable was not
        declared on the settings file.
        """
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user_two, question=question)
        qa_user = UserQAProfile.objects.get(user_id=self.user)
        qa_user_two = UserQAProfile.objects.get(user_id=self.user_two)
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        response = self.client.post(reverse('qa_answer_question',
                                    kwargs={'answer_id': answer.id}))
        qa_user.refresh_from_db()
        qa_user_two.refresh_from_db()
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        self.assertEqual(response.status_code, 302)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_QUESTION': 4}})
    def test_affect_reputation_when_creating_question(self):
        """
        This test validates than the view alters properly the right QA user
        profile when it updates the reputation points at the moment of
        an answer acceptance.
        """
        qa_user = UserQAProfile.objects.get(user=self.user)
        qa_user_two = UserQAProfile.objects.get(user=self.user_two)
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        response = self.client.post(
            reverse('qa_create_question'),
            {'title': 'Qtitle', 'description': 'babla', 'tags': 'test tag'})
        self.assertEqual(response.status_code, 302)
        qa_user.refresh_from_db()
        qa_user_two.refresh_from_db()
        self.assertEqual(qa_user.points, 4)
        self.assertEqual(qa_user_two.points, 0)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_ANSWER': 4}})
    def test_affect_reputation_when_creating_anwer(self):
        """
        This test validates than the view alters properly the right QA user
        profile at the creation point of the instance.
        """
        qa_user = UserQAProfile.objects.get(user=self.user)
        qa_user_two = UserQAProfile.objects.get(user=self.user_two)
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        question = Question.objects.create(
            title='a title', description='bla', user=self.user)
        response = self.client.post(
            reverse('qa_create_answer', kwargs={'question_id': question.pk}),
            {'question': question, 'answer_text': 'some_text_here'})
        self.assertEqual(response.status_code, 302)
        qa_user.refresh_from_db()
        qa_user_two.refresh_from_db()
        self.assertEqual(qa_user.points, 4)
        self.assertEqual(qa_user_two.points, 0)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_ANSWER_COMMENT': 4}})
    def test_affect_reputation_when_creating_answercomment(self):
        """
        This test validates than the view alters properly the right QA user
        profile at the creation point of the instance.
        """
        qa_user = UserQAProfile.objects.get(user=self.user)
        qa_user_two = UserQAProfile.objects.get(user=self.user_two)
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        answer = Answer.objects.create(
            answer_text='a title', user=self.user, question=question)
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        response = self.client.post(
            reverse('qa_create_answer_comment',
                    kwargs={'answer_id': answer.id}),
            {'comment_text': 'a description'})
        self.assertEqual(response.status_code, 302)
        qa_user.refresh_from_db()
        qa_user_two.refresh_from_db()
        self.assertEqual(qa_user.points, 4)
        self.assertEqual(qa_user_two.points, 0)

    @override_settings(QA_SETTINGS={'reputation': {'CREATE_QUESTION_COMMENT': 4}})
    def test_affect_reputation_when_creating_questioncomment(self):
        """
        This test validates than the view alters properly the right QA user
        profile at the creation point of the instance.
        """
        qa_user = UserQAProfile.objects.get(user=self.user)
        qa_user_two = UserQAProfile.objects.get(user=self.user_two)
        question = Question.objects.create(
            title='a title', description='bla', user=self.user_two)
        self.assertEqual(qa_user.points, 0)
        self.assertEqual(qa_user_two.points, 0)
        response = self.client.post(
            reverse('qa_create_question_comment',
                    kwargs={'question_id': question.pk}),
            {'comment_text': 'some_text_here'})
        self.assertEqual(response.status_code, 302)
        qa_user.refresh_from_db()
        qa_user_two.refresh_from_db()
        self.assertEqual(qa_user.points, 4)
        self.assertEqual(qa_user_two.points, 0)
