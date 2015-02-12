from django.conf.urls import patterns, include, url
from django.contrib import admin

from qa import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^q/(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^answer/(?P<question_id>\d+)/$', views.answer, name='answer'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$', views.add, name='add'),
    url(r'^answer/$', views.add_answer, name='add_answer'),
    url(r'^vote/(?P<user_id>\d+)/(?P<answer_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$', views.vote, name='vote'),
    url(r'^comment/(?P<answer_id>\d+)/$', views.comment, name='comment'),
    url(r'^search/$', views.search, name='search'),
    url(r'^thumb/(?P<user_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$', views.thumb, name='thumb'),

    url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url('^markdown/', include( 'django_markdown.urls')),

)
