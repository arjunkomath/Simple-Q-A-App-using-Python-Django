from django.contrib import admin
from qa.models import Question, Answer, Comment, Tag, Voter
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Question)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Voter)
