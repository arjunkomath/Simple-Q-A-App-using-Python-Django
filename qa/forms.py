from qa.models import Question, UserQAProfile
from django import forms


class QuestionForm(forms.ModelForm):
    new_tags = forms.CharField()

    class Meta:
        model = Question
        fields = ('title', 'description', 'new_tags')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserQAProfile
        fields = ('website', 'picture')
