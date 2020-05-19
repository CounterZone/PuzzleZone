from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import Question
from . import forms
# Create your views here.
def puzzle_display_page(request,id,section=None):
    try:
        if id=="new":
            q=Question.objects.get(name=id)
        else:
            q=Question.objects.get(id=id)
    except:
        return HttpResponse('<h1>Page was not found</h1>')
    view_permission=(request.user.is_superuser) or (q.name!="new" and((q.audited==Question.ACCEPTED) \
                    or (request.user.is_authenticated and request.user.username==q.creator.username)))
    edit_permission= (request.user.is_superuser) or (request.user.is_authenticated and \
                    (q.name=="new" or request.user.username==q.creator.username))
    if request.method=="POST":
        if section in ["edit","edit_solution","edit_test"] and edit_permission:
            instance=q if id!="new" else None
            posted_question=forms.PostQuestion(request.POST,instance=instance)

            if posted_question.is_valid():
                p=posted_question.save(False)
                if posted_question.cleaned_data["isdraft"]:
                    p.audited=Question.DRAFT
                else:
                    p.audited=Question.SUBMITTED
                p.save()
            return redirect("/puzzles/"+str(posted_question.instance.id))
    elif request.method=="GET":
        if not section:
            section="description"
        if section in ["description","solution"] and id!="new":
            if view_permission:
                context=vars(q)
                context["section"]=section
                return HttpResponse(render(request,'puzzle/puzzle_display_page.html',context={"section":section,"question":context}))
            else:
                pass # redirect
        elif section in ["edit","edit_solution","edit_test"]:
            if edit_permission:
                context=vars(q)
                return HttpResponse(render(request,'puzzle/puzzle_edit_page.html',context={"section":section,"question":context,"question_form":forms.PostQuestion(auto_id='f_%s')}))
            else:
                pass # redirect
        else:
            return HttpResponse('<h1>Page was not found</h1>')
