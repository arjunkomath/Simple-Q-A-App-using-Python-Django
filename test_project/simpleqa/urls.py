from django.conf.urls import include, url
from django.contrib import admin

from core.views import register, user_login, user_logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^', include('qa.urls')),
    ]
