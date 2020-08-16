from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import Question,Submission
from django.core.paginator import Paginator

from . import forms
# Create your views here.
def puzzle_display_page(request,id,section=None):
    try:
        if id=="new":
            q=Question.objects.get(name='new')
        else:
            q=Question.objects.get(id=id)
            if q.name=='new':
                throw()
    except:
        return HttpResponse('<h1>Page was not found</h1>')
    view_permission=(request.user.is_superuser) or (q.name!="new" and((q.audited==Question.ACCEPTED) \
                    or (request.user.is_authenticated and request.user.username==q.creator.username)))
    edit_permission= (request.user.is_superuser) or (request.user.is_authenticated and \
                    (q.name=="new" or (request.user.username==q.creator.username and q.audited==Question.DRAFT)))
    if request.method=="POST":
        if section in ["edit","edit_solution","edit_test"] and edit_permission:
            instance=q if q.name!='new' else None
            posted_question=forms.PostQuestion(request.POST,instance=instance)
            if posted_question.is_valid():
                p=posted_question.save(False)
                if p.name=="new":
                    return HttpResponse('<h1>Invalid title</h1>')
                if posted_question.cleaned_data["isdraft"]:
                    p.audited=Question.DRAFT
                else:
                    p.audited=Question.SUBMITTED
                p.save()
            else:
                return HttpResponse('<h1>Invalid submission</h1>')
            return redirect("/puzzles/"+str(posted_question.instance.id)+'/edit')
    elif request.method=="GET":
        if not section:
            section="description"
        if section in ["description","solution"] and id!="new":
            if view_permission:
                context=vars(q)
                context["section"]=section
                return HttpResponse(render(request,'puzzle/display/'+section+'.html',context={"section":section,"question":context}))
            else:
                pass # redirect
        elif section in ["edit","edit_solution","edit_test"]:
            if edit_permission:
                context=vars(q)
                return HttpResponse(render(request,'puzzle/display/'+section+'.html',context={"section":section,"question":context,"question_form":forms.PostQuestion(auto_id='f_%s')}))
            else:
                pass # redirect
        else:
            return HttpResponse('<h1>Page was not found</h1>')

def puzzle_list_page(request):
    q_list = Question.objects.filter(audited=Question.ACCEPTED).exclude(name='new').values('name','creator','have_solution')
    paginator = Paginator(q_list, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'puzzle/puzzle_list.html',context={'page_obj':page_obj,'start_index':page_obj.start_index()})


def puzzle_submission_page(request,id,submission_id=None):
    q=Question.objects.get(id=id)
    if q.name=='new':
        return HttpResponse('<h1>Page was not found</h1>')
    context=vars(q)
    if submission_id==None:
        sub_list=Submission.objects.filter(question__id=id,private=False)
        user_sub_list=Submission.objects.filter(creator__id=request.user.id) if request.user else None
        return HttpResponse(render(request,'puzzle/display/submission_list.html',context={"section":'submission',"question":context}))# add context
    else:
        sub=Submission.objects.get(id=submission_id)
        view_permission=sub.question.id==q.id and  ((request.user.is_superuser) or \
            (q.name!="new" and((q.private==False) or (request.user.id==sub.creator.id))))
        if view_permission:
            return HttpResponse(render(request,'puzzle/display/submission_view.html',context={"section":'submission',"question":context,"submission":vars(sub)}))# add context
