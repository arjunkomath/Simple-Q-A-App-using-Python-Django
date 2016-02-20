from qa.models import *
from django.contrib.auth.models import User
from django import forms

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'tags')
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
