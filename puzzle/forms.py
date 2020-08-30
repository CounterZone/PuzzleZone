from django import forms
from puzzle.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PostQuestion(forms.ModelForm):
    isdraft = forms.BooleanField(required=False)
    class Meta:
        model=Question
        fields=["name","description","pre_solution","test_cases","test_code","solution","solution_code"]
class PostDiscussion(forms.ModelForm):
    class Meta:
        model=Discussion
        fields=["title","content"]

class PostComment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["content"]

class Signup(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
