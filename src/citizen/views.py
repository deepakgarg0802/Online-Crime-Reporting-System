from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import logout

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm
from case.forms import *
from .forms import UsersRegisterForm
from .models import Citizen
from police.views import *


def login_view(request):
    if  str(request.user.__class__.__name__)=="Citizen":
        return redirect('/citizen/dashboard')

    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/citizen/dashboard")
    return render(request, "citizen/login.html",{'form':form})

def dashboard(request):
    if not request.user.is_authenticated() :
        return redirect("/citizen")
    
    total=Case.objects.filter(userid=request.user).count()
    pending=Case.objects.filter(userid=request.user,approved=False).count()
    solved=Case.objects.filter(userid=request.user,solved=True).count()
    inprogress=Case.objects.filter(userid=request.user,approved=True,solved=False).count()

    
    context={'citizen':request.user,"total":total,"pending":pending,"solved":solved,"inprogress":inprogress}
    return render(request,'citizen/dashboard.html',context)


def citizen_logout(request):
    logout(request)

    return redirect("/")

def create_case(request):
    if not request.user.is_authenticated():
        return redirect("/citizen")
    form = case_form(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return redirect("/citizen/dashboard")
    return render(request, "citizen/case.html", {"form": form})








def cbcview(request,sel=None):
    if not request.user.is_authenticated():
        return redirect("/citizen")
    my_object = get_object_or_404(Citizen, pk=request.user.id)
    
    if int(sel)==0:
        cases_qset=Case.objects.filter(userid=my_object)
    elif int(sel)==1:
        cases_qset=Case.objects.filter(userid=my_object,cyber_case_categories=None)
    elif int(sel)==2:
        cases_qset=Case.objects.filter(userid=my_object,case_categories=None)
    elif int(sel)==3:
        cases_qset=Case.objects.filter(userid=my_object,solved=True)
    elif int(sel)==4:
        cases_qset=Case.objects.filter(userid=my_object,approved=False)
        
    
    # print(cases_qset)
    
    context={"my_object":my_object,"cases_qset":cases_qset}
    return render(request,'citizen/case_by_cat.html',context)


from comment.models import Comment

def user_case_detail(request,id=None):
    if not request.user.is_authenticated():
        return redirect("/citizen")
    comments = Comment.objects.filter(case = id)
    my_object = get_object_or_404(Case, id=id)
    
    wqset=Witness.objects.filter(case=my_object)

   
    files = my_object.evidence_set.all()
    imglist={}
    vidlist={}
    audlist={}
    doculist={}
    others={}
    for i in files:
        

        if is_image(get_last(i.evidence.name)):
            imglist[get_last(i.evidence.name)]=i.evidence.url


        elif is_audio(get_last(i.evidence.name)):
            audlist[get_last(i.evidence.name)]=i.evidence.url
        
        elif is_video(get_last(i.evidence.name)):
            vidlist[get_last(i.evidence.name)]=i.evidence.url
        
        elif is_docu(get_last(i.evidence.name)):
            doculist[get_last(i.evidence.name)]=i.evidence.url

        else:

            others[get_last(i.evidence.name)]=i.evidence.url


        
    

    print(others)
    context={"my_object":my_object,"wqset":wqset,  "comments": comments,'files':files,"imglist":imglist,"vidlist":vidlist,"audlist":audlist,"doculist":doculist,"others":others}
    return render(request,'citizen/case_detail.html',context)




def create_cyber_case(request):
    if not request.user.is_authenticated():
        return redirect("/citizen")
    form=cyber_case_form(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return redirect("/citizen/dashboard")
    return render(request, "citizen/case.html",{"form" : form, 'cyber':True})


def register_view(request):
    form = UsersRegisterForm(request.POST or None)
    print(form)
    if form.is_valid():
        print('form validated successfully')
        user = form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        return redirect("/citizen/dashboard")
    return render(request, "citizen/register.html",{"form" : form,})



