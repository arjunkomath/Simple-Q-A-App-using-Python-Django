import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.generic import CreateView, View
from django.shortcuts import render, Http404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from qa.models import (UserQAProfile, Question, Answer, AnswerVote,
                       QuestionVote, Comment)
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


class CreateCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given answer
    """
    template_name = 'qa/create_comment.html'
    model = Comment
    success_url = '/'
    fields = ['comment_text']

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.answer_id = self.kwargs['answer_id']
        return super(CreateCommentView, self).form_valid(form)


class VoteView(View):
    """
    Base class to create a vote for a given model (question/answer)
    """
    model = None
    template_name = ''

    def post(self, request, object_id):
        vote_target = get_object_or_404(self.model, object_id)
        if vote_target.user == request.user:
            raise ValidationError(
                'Sorry, voting for your own answer is not possible.')

        else:
            try:
                vote = self.model(request.user, answer)
                vote.full_clean()
                vote.save()
            except ValidationError:
                pass  # vote object already exists


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


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question.views += 1
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
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            answers = paginator.page(paginator.num_pages)

    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'qa/detail.html',
                  {'answers': answers, 'question': question}, )


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
