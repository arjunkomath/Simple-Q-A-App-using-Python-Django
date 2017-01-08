from qa.models import Question
from django.conf import settings
from django import forms


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if hasattr(settings, 'QA_DESCRIPTION_OPTIONAL'):
            self.fields['description'].required = not settings.QA_DESCRIPTION_OPTIONAL
