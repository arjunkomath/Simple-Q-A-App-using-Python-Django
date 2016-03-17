from qa.models import Question, UserQAProfile
from django import forms


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'tags')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserQAProfile
        fields = ('website', 'picture')
