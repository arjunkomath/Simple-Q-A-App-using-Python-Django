import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.generic import CreateView, View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from qa.models import (UserQAProfile, Question, Answer, AnswerVote,
                       QuestionVote, AnswerComment, QuestionComment)
from .mixins import LoginRequired


class CreateQuestionView(LoginRequired, CreateView):
    """
    View to handle the creation of a new question
    """
    template_name = 'qa/create_question.html'
    model = Question
    success_url = '/'
    fields = ['title', 'description', 'tags']

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)


class CreateAnswerView(LoginRequired, CreateView):
    """
    View to create new answers for a given question
    """
    template_name = 'qa/create_answer.html'
    model = Answer
    success_url = '/'
    fields = ['answer_text']

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)


class CreateAnswerCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given answer
    """
    template_name = 'qa/create_comment.html'
    model = AnswerComment
    fields = ['comment_text']

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.answer_id = self.kwargs['answer_id']
        return super(CreateAnswerCommentView, self).form_valid(form)

    def get_success_url(self):
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

    def form_valid(self, form):
        """
        Creates the required relationship between question
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateQuestionCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('qa_detail', kwargs={'pk': self.kwargs['question_id']})


class QuestionDetailView(DetailView):
    """
    View to call a question and to render all the details about that question.
    """
    model = Question
    template_name = 'qa/detail_question.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['last_comments'] = self.object.questioncomment_set.order_by(
            'pub_date')[:5]
        return context


class ParentVoteView(View):
    """
    Base class to create a vote for a given model (question/answer)
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
            vote, created = self.vote_model.objects.get_or_create(defaults={'value': upvote},**object_kwargs)
            if created:
                vote_target.votes += 1 if upvote else -1
            elif not created:
                if vote.value == upvote:
                    vote.delete()
                    vote_target.votes += -1 if upvote else 1
                else:
                    vote_target.votes += 2 if upvote else -2
                    vote.value = upvote
                    vote.save()
            vote_target.save()
        print request.POST
        next_url = request.POST.get('next', None)
        if next_url is not None:
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


def search(request):
    if request.method == 'POST':
        word = request.POST['word']
        latest_question_list = Question.objects.filter(title__contains=word)
        paginator = Paginator(latest_question_list, 10)
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            questions = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            questions = paginator.page(paginator.num_pages)

        latest_noans_list = Question.objects.order_by('-pub_date').filter(
            tags__slug__contains=word, answer__isnull=True)[:10]
        top_questions = Question.objects.order_by('-reward').filter(
            tags__slug__contains=word, answer__isnull=True, reward__gte=1)[:10]
        count = Question.objects.count
        count_a = Answer.objects.count
        template = loader.get_template('qa/index.html')
        context = RequestContext(request, {
            'questions': questions,
            'totalcount': count,
            'anscount': count_a,
            'noans': latest_noans_list,
            'reward': top_questions,
        })
    return HttpResponse(template.render(context))


def tag(request, tag):
    word = tag
    latest_question_list = Question.objects.filter(tags__slug__contains=word)
    paginator = Paginator(latest_question_list, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    latest_noans_list = Question.objects.order_by('-pub_date').filter(
        tags__slug__contains=word, answer__isnull=True)[:10]
    top_questions = Question.objects.order_by('-reward').filter(
        tags__slug__contains=word, answer__isnull=True, reward__gte=1)[:10]
    count = Question.objects.count
    count_a = Answer.objects.count
    template = loader.get_template('qa/index.html')
    context = RequestContext(request, {
        'questions': questions,
        'totalcount': count,
        'anscount': count_a,
        'noans': latest_noans_list,
        'reward': top_questions,
    })
    return HttpResponse(template.render(context))


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    latest_noans_list = Question.objects.order_by('-pub_date').filter(
        answer__isnull=True)[:10]
    top_questions = Question.objects.order_by('-reward').filter(
        answer__isnull=True, reward__gte=1)[:10]
    count = Question.objects.count
    count_a = Answer.objects.count
    paginator = Paginator(latest_question_list, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    template = loader.get_template('qa/index.html')
    context = RequestContext(request, {
        'questions': questions,
        'totalcount': count,
        'anscount': count_a,
        'noans': latest_noans_list,
        'reward': top_questions,
    })
    return HttpResponse(template.render(context))


def profile(request, user_id):
    user_ob = get_user_model().objects.get(id=user_id)
    user = UserQAProfile.objects.get(user=user_ob)
    return render(request, 'qa/profile.html', {'user': user})


def vote(request, user_id, answer_id, question_id, op_code):
    user_ob = get_user_model().objects.get(id=user_id)
    user = UserQAProfile.objects.get(user=user_ob)
    answer = Answer.objects.get(pk=answer_id)
    question = Question.objects.get(pk=question_id)
    answer_list = question.answer_set.order_by('-votes')
    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    if Answer.objects.filter(id=answer_id, user=user_ob).exists():
        return render(request, 'qa/detail.html',
                      {'question': question, 'answers': answers,
                       'message': "You cannot vote on your answer!"})

    if Voter.objects.filter(answer_id=answer_id, user=user).exists():
        return render(request, 'qa/detail.html',
                      {'question': question, 'answers': answers,
                       'message': "You've already cast vote on this answer!"})

    if op_code == '0':
        answer.votes += 1
        u = answer.user_data
        u.points += 10
        u.points += question.reward
        u.save()

    if op_code == '1':
        answer.votes -= 1
        u = answer.user_data
        u.points -= 10
        u.save()

    answer.save()
    answer_list = question.answer_set.order_by('-votes')
    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    v = Voter()
    v.user = user
    v.answer = answer
    v.save()

    return render(request, 'qa/detail.html',
                  {'question': question, 'answers': answers})


def thumb(request, user_id, question_id, op_code):
    user_ob = get_user_model().objects.get(id=user_id)
    user = UserQAProfile.objects.get(user=user_ob)
    question = Question.objects.get(pk=question_id)
    answer_list = question.answer_set.order_by('-votes')
    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')

    try:
        answers = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    if QVoter.objects.filter(question_id=question_id, user=user_ob).exists():
        return render(request, 'qa/detail.html',
                      {'question': question, 'answers': answers,
                       'message': "You've already cast vote on this question!"}
                      )

    if op_code == '0':
        question.reward += 5
        user.points += 5
        user.save()

    if op_code == '1':
        question.reward -= 5
        user.points -= 5
        user.save()

    question.save()
    answer_list = question.answer_set.order_by('-votes')
    paginator = Paginator(answer_list, 10)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)

    v = QVoter()
    v.user = user_ob
    v.question = question
    v.save()
    return render(request, 'qa/detail.html',
                  {'question': question, 'answers': answers})
