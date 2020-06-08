from django import forms
from puzzle.models import *
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
