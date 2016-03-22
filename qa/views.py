import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.generic import CreateView
from django.shortcuts import render, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model

from qa.models import UserQAProfile, Question, Answer, Voter, QVoter, Comment
from .mixins import LoginRequired

# Commented lines because bad imported and unnused, but perhaps will be need
# later so better to keep them here... for now.
# from django.shortcuts import render, get_object_or_404, render_to_response
# from django.core.mail import send_mail
# from django.views.generic.edit import ModelFormMixin
# from django.core.urlresolvers import reverse
# from qa.forms import QuestionForm, UserProfileForm
# from qa.forms import QuestionForm


class CreateQuestionView(LoginRequired, CreateView):
    """
    View to handle the creation of a new question
    """
    template_name = 'qa/create_question.html'
    model = Question
    success_url = '/'
    fields = ['title', 'description']

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

    def get_context_data(self, **kwargs):
        """
        Add question_id to context
        """
        kwargs.setdefault('question_id', self.kwargs.get('question_id'))
        return super(CreateAnswerView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)


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


def comment(request, answer_id):  # requires login

    if request.user.is_anonymous():
        return HttpResponseRedirect("/login/")

    if request.method == 'POST':
        comment_text = request.POST['comment']
        user_id = request.POST['user']
        user_ob = get_user_model().objects.get(id=user_id)
        user = UserQAProfile.objects.get(user=user_ob)
        user.points += 1
        user.save()
        if comment_text.strip() == '':
            return render(request, 'qa/comment.html',
                          {'answer_id': answer_id, 'message': 'Empty'})

        pub_date = datetime.datetime.now()
        a = Answer.objects.get(pk=answer_id)
        q_id = a.question_id
        c = Comment()
        c.answer = a
        c.comment_text = comment_text
        c.pub_date = pub_date
        c.user = user_ob
        c.save()
        try:
            question = Question.objects.get(pk=q_id)
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

    template = loader.get_template('qa/comment.html')
    context = RequestContext(request, {'answer_id': answer_id})
    return HttpResponse(template.render(context))


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


def answer(request, question_id):  # requires login
    if request.user.is_anonymous():
        return HttpResponseRedirect("/login/")

    try:
        question = Question.objects.get(pk=question_id)

    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'qa/answer.html', {'question': question})



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
