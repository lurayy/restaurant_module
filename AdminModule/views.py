from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserForm, LoginForm
from ApiModule.models import CustomUser
import json
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def check(user):
    try:
        if user.is_rmanager == True:
            return True    
        else:
            return False
    except:
        return False


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/reception')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/reception')
                else:
                    return HttpResponseRedirect('login')   
        else:
            form = LoginForm()
            return render (request, 'ReceptionModule/login.html',{'form':form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@user_passes_test(check,login_url='/')
def user_registration(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            print(user)
            print("user created")
            return HttpResponseRedirect('/admin')
        else:
            print("error on the forms")
            return render(request, 'AdminModule/staff_id_form.html', { 'user_form':user_form})
    else:
        user_form = UserForm()
        return render(request, 'AdminModule/staff_id_form.html', { 'user_form':user_form})


@user_passes_test(check,login_url='/')
def user_manage(request):
    return render(request, 'AdminModule/admin_panel.html')        


@user_passes_test(check, login_url="/")
def admin_panel(request):
    return render(request, 'AdminModule/admin_panel.html')