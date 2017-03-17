from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.QuestionIndexView.as_view(), name='qa_index'),

    url(r'^question/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(), name='qa_detail'),

    url(r'^question/(?P<pk>\d+)/(?P<slug>[-_\w]+)/$',
        views.QuestionDetailView.as_view(), name='qa_detail'),

    url(r'^question/answer/(?P<answer_id>\d+)/$',
        views.AnswerQuestionView.as_view(), name='qa_answer_question'),

    url(r'^question/close/(?P<question_id>\d+)/$',
        views.CloseQuestionView.as_view(), name='qa_close_question'),

    url(r'^new-question/$', views.CreateQuestionView.as_view(),
        name='qa_create_question'),

    url(r'^edit-question/(?P<question_id>\d+)/$',
        views.UpdateQuestionView.as_view(),
        name='qa_update_question'),

    url(r'^answer/(?P<question_id>\d+)/$',
        views.CreateAnswerView.as_view(), name='qa_create_answer'),

    url(r'^answer/edit/(?P<answer_id>\d+)/$',
        views.UpdateAnswerView.as_view(), name='qa_update_answer'),

    url(r'^vote/question/(?P<object_id>\d+)/$',
        views.QuestionVoteView.as_view(), name='qa_question_vote'),

    url(r'^vote/answer/(?P<object_id>\d+)/$',
        views.AnswerVoteView.as_view(), name='qa_answer_vote'),

    url(r'^comment-answer/(?P<answer_id>\d+)/$',
        views.CreateAnswerCommentView.as_view(),
        name='qa_create_answer_comment'),

    url(r'^comment-question/(?P<question_id>\d+)/$',
        views.CreateQuestionCommentView.as_view(),
        name='qa_create_question_comment'),

    url(r'^comment-question/edit/(?P<comment_id>\d+)/$',
        views.UpdateQuestionCommentView.as_view(),
        name='qa_update_question_comment'),

    url(r'^comment-answer/edit/(?P<comment_id>\d+)/$',
        views.UpdateAnswerCommentView.as_view(),
        name='qa_update_answer_comment'),

    url(r'^search/$', views.QuestionsSearchView.as_view(), name='qa_search'),

    url(r'^tag/(?P<tag>[-\w]+)/$',
        views.QuestionsByTagView.as_view(), name='qa_tag'),

    url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='qa_profile'),

    url('^markdown/', include('django_markdown.urls')),

    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

]
