from django.contrib import admin
from qa.models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(UserProfile)
