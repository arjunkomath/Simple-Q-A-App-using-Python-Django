from django.conf.urls import url, include
from django.contrib import admin

from core.views import register, user_login, user_logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^', include('qa.urls')),
    ]
