from django import forms
from puzzle.models import *
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


class PostQuestion(forms.ModelForm):
    isdraft = forms.BooleanField(required=False)
    class Meta:
        model=Question
        fields=["name","description","pre_solution","test_cases","test_code","solution","solution_code","have_solution"]
    def clean(self):
        super().clean()
        self.cleaned_data = dict([ (k,v) for k,v in self.cleaned_data.items() if v != 'null' ])

class PostDiscussion(forms.ModelForm):
    class Meta:
        model=Discussion
        fields=["title","content"]

class PostComment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["content"]

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileChangeForm(SetPasswordForm):
    username=forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileChangeForm, self).__init__(user,*args, **kwargs)
        self.order_fields([
            'username',
            'email',
            'new_password1',
            'new_password2'])
        self.fields['email'].initial=user.email
        self.fields['username'].initial=user.username
