from qa.models import UserQAProfile
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserQAProfile
        fields = ('website', 'picture')
