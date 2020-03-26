import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, UpdateView, View
from hitcount.views import HitCountDetailView
from qa.models import (Answer, AnswerComment, AnswerVote, Question,
                       QuestionComment, QuestionVote, UserQAProfile)
from taggit.models import Tag, TaggedItem

from .forms import QuestionForm
from .mixins import AuthorRequiredMixin, LoginRequired
from .utils import question_score

try:
    qa_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and\
        settings.QA_SETTINGS['qa_messages']

except AttributeError:  # pragma: no cover
    qa_messages = False

if qa_messages:
    from django.contrib import messages


"""Dear maintainer:

Once you are done trying to 'optimize' this routine, and have realized what a
terrible mistake that was, please increment the following counter as a warning
to the next guy:

total_hours_wasted_here = 2
"""


class AnswerQuestionView(LoginRequired, View):
    """
    View to select an answer as the satisfying answer to the question,
    validating than the user who created que
    question is the only one allowed to make those changes.
    """
    model = Answer

    def post(self, request, answer_id):
        answer = get_object_or_404(self.model, pk=answer_id)
        if answer.question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question.")

        else:
            answer.question.answer_set.update(answer=False)
            answer.answer = True
            answer.save()

            try:
                points = settings.QA_SETTINGS['reputation']['ACCEPT_ANSWER']

            except KeyError:
                points = 0

            qa_user = UserQAProfile.objects.get(user=answer.user)
            qa_user.modify_reputation(points)

        next_url = request.POST.get('next', '')
        if next_url is not '':
            return redirect(next_url)

        else:
            return redirect(reverse('qa_index'))


class CloseQuestionView(LoginRequired, View):
    """View to
    mark the question as closed, validating than the user who created que
    question is the only one allowed to make those changes.
    """
    model = Question

    def post(self, request, question_id):
        question = get_object_or_404(self.model, pk=question_id)
        if question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question.")
        else:
            if not question.closed:
                question.closed = True

            else:
                raise ValidationError("Sorry, this question is already closed")

            question.save()

        next_url = request.POST.get('next', '')
        if next_url is not '':
            return redirect(next_url)

        else:
            return redirect(reverse('qa_index'))


class QuestionIndexView(ListView):
    """CBV to render the index view
    """
    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/index.html'
    ordering = '-pub_date'

    def get_context_data(self, *args, **kwargs):
        context = super(
            QuestionIndexView, self).get_context_data(*args, **kwargs)
        noans = Question.objects.order_by('-pub_date').filter(
            answer__isnull=True).select_related('user')\
            .annotate(num_answers=Count('answer', distinct=True),
                      num_question_comments=Count('questioncomment',
                      distinct=True))
        context['totalcount'] = Question.objects.count()
        context['anscount'] = Answer.objects.count()
        paginator = Paginator(noans, 10)
        page = self.request.GET.get('noans_page')
        context['active_tab'] = self.request.GET.get('active_tab', 'latest')
        tabs = ['latest', 'unans', 'reward']
        context['active_tab'] = 'latest' if context['active_tab'] not in\
            tabs else context['active_tab']
        try:
            noans = paginator.page(page)

        except PageNotAnInteger:
            noans = paginator.page(1)

        except EmptyPage:  # pragma: no cover
            noans = paginator.page(paginator.num_pages)

        context['totalnoans'] = paginator.count
        context['noans'] = noans
        context['reward'] = Question.objects.order_by('-reward').filter(
            reward__gte=1)[:10]
        question_contenttype = ContentType.objects.get_for_model(Question)
        items = TaggedItem.objects.filter(content_type=question_contenttype)
        context['tags'] = Tag.objects.filter(
            taggit_taggeditem_items__in=items).order_by('-id').distinct()[:10]

        return context

    def get_queryset(self):
        queryset = super(QuestionIndexView, self).get_queryset()\
            .select_related('user')\
            .annotate(num_answers=Count('answer', distinct=True),
                      num_question_comments=Count('questioncomment',
                      distinct=True))
        return queryset


class QuestionsSearchView(QuestionIndexView):
    """
    Display a ListView page inherithed from the QuestionIndexView filtered by
    the search query and sorted by the different elements aggregated.
    """

    def get_queryset(self):
        result = super(QuestionsSearchView, self).get_queryset()
        query = self.request.GET.get('word', '')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)))

        return result

    def get_context_data(self, *args, **kwargs):
        context = super(
            QuestionsSearchView, self).get_context_data(*args, **kwargs)
        context['totalcount'] = Question.objects.count
        context['anscount'] = Answer.objects.count
        context['noans'] = Question.objects.order_by('-pub_date').filter(
            answer__isnull=True)[:10]
        context['reward'] = Question.objects.order_by('-reward').filter(
            reward__gte=1)[:10]
        return context


class QuestionsByTagView(ListView):
    """View to call all the questions clasiffied under one specific tag.
    """
    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/index.html'

    def get_queryset(self, **kwargs):
        return Question.objects.filter(tags__slug=self.kwargs['tag'])

    def get_context_data(self, *args, **kwargs):
        context = super(
            QuestionsByTagView, self).get_context_data(*args, **kwargs)
        context['active_tab'] = self.request.GET.get('active_tab', 'latest')
        tabs = ['latest', 'unans', 'reward']
        context['active_tab'] = 'latest' if context['active_tab'] not in\
            tabs else context['active_tab']
        context['totalcount'] = Question.objects.count
        context['anscount'] = Answer.objects.count
        context['noans'] = Question.objects.order_by('-pub_date').filter(
            tags__name__contains=self.kwargs['tag'], answer__isnull=True)[:10]
        context['reward'] = Question.objects.order_by('-reward').filter(
            tags__name__contains=self.kwargs['tag'],
            reward__gte=1)[:10]
        context['totalnoans'] = len(context['noans'])
        return context


class CreateQuestionView(LoginRequired, CreateView):
    """
    View to handle the creation of a new question
    """
    template_name = 'qa/create_question.html'
    message = _('Thank you! your question has been created.')
    form_class = QuestionForm

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse('qa_index')


class UpdateQuestionView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question
    """
    template_name = 'qa/update_question.html'
    model = Question
    pk_url_kwarg = 'question_id'
    fields = ['title', 'description', 'tags']

    def get_success_url(self):
        question = self.get_object()
        return reverse('qa_detail', kwargs={'pk': question.pk})


class CreateAnswerView(LoginRequired, CreateView):
    """
    View to create new answers for a given question
    """
    template_name = 'qa/create_answer.html'
    model = Answer
    fields = ['answer_text']
    message = _('Thank you! your answer has been posted.')

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse('qa_detail', kwargs={'pk': self.kwargs['question_id']})


class UpdateAnswerView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question answer
    """
    template_name = 'qa/update_answer.html'
    model = Answer
    pk_url_kwarg = 'answer_id'
    fields = ['answer_text']

    def get_success_url(self):
        answer = self.get_object()
        return reverse('qa_detail', kwargs={'pk': answer.question.pk})


class CreateAnswerCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given answer
    """
    template_name = 'qa/create_comment.html'
    model = AnswerComment
    fields = ['comment_text']
    message = _('Thank you! your comment has been posted.')

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.answer_id = self.kwargs['answer_id']
        return super(CreateAnswerCommentView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        question_pk = Answer.objects.get(
            id=self.kwargs['answer_id']).question.pk
        return reverse('qa_detail', kwargs={'pk': question_pk})


class CreateQuestionCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given question
    """
    template_name = 'qa/create_comment.html'
    model = QuestionComment
    fields = ['comment_text']
    message = _('Thank you! your comment has been posted.')

    def form_valid(self, form):
        """
        Creates the required relationship between question
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateQuestionCommentView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            messages.success(self.request, self.message)

        return reverse('qa_detail', kwargs={'pk': self.kwargs['question_id']})


class UpdateQuestionCommentView(LoginRequired,
                                AuthorRequiredMixin, UpdateView):
    """
    Updates the comment question
    """
    template_name = 'qa/create_comment.html'
    model = QuestionComment
    pk_url_kwarg = 'comment_id'
    fields = ['comment_text']

    def get_success_url(self):
        question_comment = self.get_object()
        return reverse('qa_detail',
                       kwargs={'pk': question_comment.question.pk})


class UpdateAnswerCommentView(UpdateQuestionCommentView):
    """
    Updates the comment answer
    """
    model = AnswerComment

    def get_success_url(self):
        answer_comment = self.get_object()
        return reverse('qa_detail',
                       kwargs={'pk': answer_comment.answer.question.pk})


class QuestionDetailView(HitCountDetailView):
    """
    View to call a question and to render all the details about that question.
    """
    model = Question
    template_name = 'qa/detail_question.html'
    context_object_name = 'question'
    slug_field = 'slug'
    try:
        count_hit = settings.QA_SETTINGS['count_hits']

    except KeyError:
        count_hit = True

    def get_context_data(self, **kwargs):
        answers = self.object.answer_set.all().order_by('pub_date')
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['last_comments'] = self.object.questioncomment_set.order_by(
            'pub_date')[:5]
        context['answers'] = list(answers.select_related(
            'user').select_related(
            'user__userqaprofile')
            .annotate(answercomment_count=Count('answercomment')))
        return context

    def get(self, request, **kwargs):
        my_object = self.get_object()
        slug = kwargs.get('slug', '')
        if slug != my_object.slug:
            kwargs['slug'] = my_object.slug
            return redirect(reverse('qa_detail', kwargs=kwargs))

        else:
            return super(QuestionDetailView, self).get(request, **kwargs)

    def get_object(self):
        question = super(QuestionDetailView, self).get_object()
        return question


class ParentVoteView(View):
    """Base class to create a vote for a given model (question/answer)
    """
    model = None
    vote_model = None

    def get_vote_kwargs(self, user, vote_target):
        """
        This takes the user and the vote and adjusts the kwargs
        depending on the used model.
        """
        object_kwargs = {'user': user}
        if self.model == Question:
            target_key = 'question'

        elif self.model == Answer:
            target_key = 'answer'

        else:
            raise ValidationError('Not a valid model for votes')

        object_kwargs[target_key] = vote_target
        return object_kwargs

    def post(self, request, object_id):
        vote_target = get_object_or_404(self.model, pk=object_id)
        if vote_target.user == request.user:
            raise ValidationError(
                'Sorry, voting for your own answer is not possible.')

        else:
            upvote = request.POST.get('upvote', None) is not None
            object_kwargs = self.get_vote_kwargs(request.user, vote_target)
            vote, created = self.vote_model.objects.get_or_create(
                defaults={'value': upvote},
                **object_kwargs)
            if created:
                vote_target.user.userqaprofile.points += 1 if upvote else -1
                if upvote:
                    vote_target.positive_votes += 1

                else:
                    vote_target.negative_votes += 1

            else:
                if vote.value == upvote:
                    vote.delete()
                    vote_target.user.userqaprofile.points += -1 if upvote else 1
                    if upvote:
                        vote_target.positive_votes -= 1

                    else:
                        vote_target.negative_votes -= 1

                else:
                    vote_target.user.userqaprofile.points += 2 if upvote else -2
                    vote.value = upvote
                    vote.save()
                    if upvote:
                        vote_target.positive_votes += 1
                        vote_target.negative_votes -= 1

                    else:
                        vote_target.negative_votes += 1
                        vote_target.positive_votes -= 1

            vote_target.user.userqaprofile.save()
            if self.model == Question:
                vote_target.reward = question_score(vote_target)

            if self.model == Answer:
                vote_target.question.reward = question_score(
                    vote_target.question)
                vote_target.question.save()

            vote_target.save()

        next_url = request.POST.get('next', '')
        if next_url is not '':
            return redirect(next_url)

        else:
            return redirect(reverse('qa_index'))


class AnswerVoteView(ParentVoteView):
    """
    Class to upvote answers
    """
    model = Answer
    vote_model = AnswerVote


class QuestionVoteView(ParentVoteView):
    """
    Class to upvote questions
    """
    model = Question
    vote_model = QuestionVote


def profile(request, user_id):
    user_ob = get_user_model().objects.get(id=user_id)
    user = UserQAProfile.objects.get(user=user_ob)
    context = {'user': user}
    return render(request, 'qa/profile.html', context)
