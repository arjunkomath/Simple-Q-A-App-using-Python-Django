from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='qa_index'),
    url(r'^question/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(), name='qa_detail'),
    url(r'^new-question/$', views.CreateQuestionView.as_view(),
        name='qa_create_question'),
    url(r'^answer/(?P<question_id>\d+)/$',
        views.CreateAnswerView.as_view(), name='qa_create_answer'),
    url(r'^comment-answer/(?P<answer_id>\d+)/$',
        views.CreateAnswerCommentView.as_view(),
        name='qa_create_answer_comment'),
    url(r'^comment-question/(?P<question_id>\d+)/$',
        views.CreateQuestionCommentView.as_view(),
        name='qa_create_question_comment'),
    url(r'^vote/(?P<answer_id>\d+)/$', views.vote, name='qa_vote'),
    url(r'^search/$', views.search, name='qa_search'),
    url(r'^tag/(?P<tag>[-\w]+)/$', views.tag, name='qa_tag'),
    url(r'^thumb/(?P<user_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$',
        views.thumb, name='qa_thumb'),

    url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='qa_profile'),
]
