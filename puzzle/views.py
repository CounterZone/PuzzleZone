from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect

from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

from .models import Question,Submission
from .forms import SignupForm,ProfileChangeForm,PostQuestion

from django.views.generic.list import ListView,View
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

def raise_404(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404()
    return wrap

def question_permission_check(option,question,request,check=True):
    '''
    option: 'view' or 'edit'
    if check==true, raise exceptions. otherwise return the result
    '''
    q=question
    if option=='view':
        if not ((request.user.is_superuser) or (q.name!="new" and((q.audited==Question.ACCEPTED) \
                        or (request.user.is_authenticated and request.user.username==q.creator.username)))):
            if check:
                raise PermissionDenied()
            return False
    elif option=='edit':
        if not ((request.user.is_superuser) or (request.user.is_authenticated and \
                        (q.name=="new" or (request.user.username==q.creator.username)))):
            if check:
                raise PermissionDenied()
            return False
    return True


class puzzle_display_view(View):
    @raise_404
    def post(self,request,id,section='description'):
        if id=="new":
            q=Question.objects.get(name='new')
        else:
            q=Question.objects.get(id=id)
            if q.name=='new':
                raise Http404()
        question_permission_check('edit',q,request)
        if section in ["edit","edit_solution","edit_test"]:
            instance=q if q.name!='new' else None
            posted_question=PostQuestion(request.POST,instance=instance)
            if posted_question.is_valid():
                p=posted_question.save(False)
                if p.name=="new":
                    return HttpResponse('<h1>Invalid title</h1>')
                if posted_question.cleaned_data["isdraft"]:
                    p.audited=Question.DRAFT
                else:
                    p.audited=Question.SUBMITTED
                p.creator=request.user
                p.save()
            else:
                return HttpResponse('<h1>Invalid submission</h1>')
            return redirect("/puzzles/"+str(posted_question.instance.id)+'/edit')
    @raise_404
    def get(self,request,id,section='description'):
        if id=="new":
            q=Question.objects.get(name='new')
        else:
            q=Question.objects.get(id=id)
            if q.name=='new':
                raise Http404()
        question_permission_check('view',q,request)
        if section in ["description","solution"] and id!="new":
                context=vars(q)
                context['creator']=q.creator.username
                context["section"]=section
                return HttpResponse(render(request,'puzzle/display/'+section+'.html',context={"section":section,"question":context,"edit_permission":question_permission_check('edit',q,request,check=False)}))
        elif section in ["edit","edit_solution","edit_test"]:
                question_permission_check('edit',q,request)
                context=vars(q)
                return HttpResponse(render(request,'puzzle/display/'+section+'.html',context={"section":section,"question":context,"question_form":PostQuestion(auto_id='f_%s')}))
        else:
            raise Http404('<h1>Page was not found</h1>')

class puzzle_list_view(ListView):
    model=Question
    paginate_by = 15
    template_name = 'puzzle/puzzle_list.html'
    context_object_name = 'puzzle_list'
    queryset=Question.objects.filter(audited=Question.ACCEPTED).exclude(name='new').values('name','id')
    def get_context_data(self, **kwargs):
        import os.path
        context = super().get_context_data(**kwargs)
        r=open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','Readme.md'))
        context['readme'] = str(r.read())
        r.close()
        return context


class signin_view(auth_views.LoginView):
    template_name='auth/sign_in.html'
    redirect_authenticated_user=True


class signup_view(View):
    def post(self,request):
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
    def get(self,request):
        if not request.user.is_authenticated:
            form = SignupForm()
            return render(request,'auth/sign_up.html',{'form':form})
        else:
            return redirect('/puzzles/')


class profile_view(View):
    def get(self,request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            mylist=Question.objects.filter(creator__id=request.user.id) if "my_puzzle" in request.GET else None
            return render(request,'auth/profile.html',context={'form':ProfileChangeForm(user),'page_obj':mylist})
        return redirect('/sign_in')
    def post(self,request):
        user = User.objects.get(id=request.user.id)
        form = ProfileChangeForm(user,request.POST)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('/profile/')
        else:
            return render(request,'auth/profile.html',{'form':form})


class logout_view(auth_views.LogoutView):
    next_page='/puzzles/'


class puzzle_submission_view(View):
    @raise_404
    def post(self,request,id,submission_list):
        submission_id = request.GET.get('submission')
        sub=Submission.objects.get(id=submission_id)
        edit_permission=((request.user.is_superuser) or \
            ((request.user.id==sub.creator.id)))
        if edit_permission:
            if request.POST['command']=='publish':
                sub.private=False
                sub.save()
            elif request.POST['command']=='delete':
                sub.delete()
        return redirect('/puzzles/'+str(id)+'/submission/'+submission_list)

    @raise_404
    def get(self,request,id,submission_list='user'):
        q=Question.objects.get(id=id)
        question_permission_check('view',q,request)
        submission_id = request.GET.get('submission')
        if q.name=='new':
            raise Http404("Page does not exist")
        context=vars(q)
        context['creator']=q.creator.username
        if submission_list=='public':
            sub_list=Submission.objects.filter(question__id=id,private=False)
        elif submission_list=='user':
            sub_list=Submission.objects.filter(creator__id=request.user.id) if request.user else None
        if submission_id:
            sub=Submission.objects.get(id=submission_id)
            if sub.question.id!=q.id:
                raise Http404()
            view_permission=((request.user.is_superuser) or \
                (q.name!="new" and((sub.private==False) or (request.user.id==sub.creator.id))))
            if view_permission:
                return HttpResponse(render(request,'puzzle/display/submission.html',context={"section":'submission',"question":context,'page_obj':sub_list,"submission":vars(sub),"edit_permission":question_permission_check('edit',q,request,check=False)}))# add context
            else:
                raise PermissionDenied()
        else:
            return HttpResponse(render(request,'puzzle/display/submission.html',context={"section":'submission',"question":context,'page_obj':sub_list,"edit_permission":question_permission_check('edit',q,request,check=False)}))# add context
