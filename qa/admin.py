from django.contrib import admin
from qa.models import Question, Answer, AnswerComment,\
 AnswerVote, QuestionComment  # Tag,
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Question)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
# admin.site.register(Tag)
admin.site.register(AnswerVote)
