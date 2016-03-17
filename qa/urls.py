from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^q/(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^answer/(?P<question_id>\d+)/$', views.answer, name='answer'),
    url(r'^add/$', views.add, name='add'),
    url(r'^answer/$', views.add_answer, name='add_answer'),
    url(r'^vote/(?P<user_id>\d+)/(?P<answer_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$', views.vote, name='vote'),
    url(r'^comment/(?P<answer_id>\d+)/$', views.comment, name='comment'),
    url(r'^search/$', views.search, name='search'),
    url(r'^tag/(?P<tag>\w+)/$', views.tag, name='tag'),
    url(r'^thumb/(?P<user_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$', views.thumb, name='thumb'),

    url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='profile'),
]
