from qa.models import Question
from django.conf import settings
from django import forms


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        try:
            settings.QA_SETTINGS['qa_description_optional']
            self.fields['description'].required = not settings.QA_SETTINGS[
                'qa_description_optional']

        except KeyError:
            pass
