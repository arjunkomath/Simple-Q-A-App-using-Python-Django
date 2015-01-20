from django.contrib import admin
from qa.models import *
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Question)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(UserProfile)
