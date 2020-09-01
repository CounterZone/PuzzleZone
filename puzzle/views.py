from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import Question,Submission
from django.core.paginator import Paginator
from .forms import SignupForm,ProfileChangeForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from . import forms
from django.contrib.auth import logout


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
                context['creator']=q.creator.username
                context["section"]=section
                return HttpResponse(render(request,'puzzle/display/'+section+'.html',context={"section":section,"question":context,"edit_permission":edit_permission}))
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
    q_list = Question.objects.filter(audited=Question.ACCEPTED).exclude(name='new').values('name','id')
    paginator = Paginator(q_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'puzzle/puzzle_list.html',context={'page_obj':page_obj,'start_index':page_obj.start_index()})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/puzzles/')
        else:
            return render(request,'auth/sign_up.html',{'form':form})
    elif request.method == 'GET':
        if not request.user.is_authenticated:
            form = SignupForm()
            return render(request,'auth/sign_up.html',{'form':form})
        else:
            return redirect('/puzzles/')


def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            return render(request,'auth/profile.html',context={'form':ProfileChangeForm(user)})
        return redirect('/sign_in')
    elif request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ProfileChangeForm(user,request.POST)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('/profile/')
        else:
            return render(request,'auth/profile.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('/puzzles/')


def puzzle_submission_page(request,id,submission_id=None):
    q=Question.objects.get(id=id)
    if q.name=='new':
        return HttpResponse('<h1>Page was not found</h1>')
    context=vars(q)
    context['creator']=q.creator.username
    sub_list=Submission.objects.filter(question__id=id,private=False)
    user_sub_list=Submission.objects.filter(creator__id=request.user.id) if request.user else None
    if submission_id:
        sub=Submission.objects.get(id=submission_id)
        view_permission=sub.question.id==q.id and  ((request.user.is_superuser) or \
            (q.name!="new" and((q.private==False) or (request.user.id==sub.creator.id))))
        if view_permission:
            return HttpResponse(render(request,'puzzle/display/submission.html',context={"section":'submission',"question":context,"submission":vars(sub)}))# add context
    else:
        return HttpResponse(render(request,'puzzle/display/submission.html',context={"section":'submission',"question":context}))# add context
