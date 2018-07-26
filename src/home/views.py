from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import AnonymousTipForm, AnonymousUsersLoginForm
from police.models import Criminal
from .forms import EvidenceForm
from home.models import Evidence
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import string
from .models import AnonymousUser, AnonymousTip
from django.contrib.auth import authenticate, login, logout


def gen_uname_pass():
    return (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9)),
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
            )


def upload_evidence(request,id=None):
    tip = get_object_or_404(AnonymousTip,pk=id)
    if not request.user.is_authenticated():
        raise Http404

    username = password = None
    if tip.userid:
        username = tip.userid.username
        password = tip.userid.password

    form = EvidenceForm(request.POST or None, request.FILES or None)
    print(form)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.anonymous_tip = tip
        instance.save()
        messages.success(request,'Evidence Uploaded Successfully')
        return redirect('/')

    return render(request, "anonymous/evidence.html", {"form": form, 'username':username, 'password':password})



def anonymous_tip(request):
    if request.user.is_authenticated():
        logout(request)
    form = AnonymousTipForm(request.POST or None)
    if form.is_valid():
        upload_evidence = form.cleaned_data.get("upload_evidence")
        stay_in_touch = form.cleaned_data.get("stay_in_touch")
        instance = form.save(commit = False)
        if stay_in_touch:
            username, password = gen_uname_pass()
            new_user = AnonymousUser.objects.create(username=username, password=password)
            new_user.save
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            instance.userid = new_user
            instance.save()

            if not upload_evidence:
               return render(request, "anonymous/get_cred.html", {'username':username,'password':password} )

        instance.save()
        if not upload_evidence:
            messages.success(request, "Tip Submitted Successfully")
            return redirect('/')
        else:
            return redirect(reverse('upload_anonymous_evidence', kwargs={'id': instance.pk}))
    return render(request,'anonymous/tip.html',{'form':form})



def get_interact_anonymous(request):
    user = request.user
    print(user.anonymous_tip_)


    return render(request, "", {})

def anonymous_user_login(request):
    form = AnonymousUsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        upload_evidence = form.cleaned_data.get("upload_evidence")
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect("/anonymous/dashboard")

    return render(request, "anonymous/login.html", {"form": form})


def anonymous_dashboard(request):
    if not request.user.is_authenticated() or not str(request.user.__class__.__name__)=="AnonymousUser":
        raise Http404
    return render(request,'anonymous/dashboard.html',{'citizen':request.user})



def criminal_directory(request):
    search_query = request.GET.get('q')
    var = Criminal.objects.all()
    print(var)
    if search_query:
        var = var.filter(name__contains=search_query)
    return render(request, "criminal_directory.html",{'var':var})
