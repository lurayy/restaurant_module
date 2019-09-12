from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserForm, LoginForm
from ApiModule.models import CustomUser, StaffPosition
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


@user_passes_test(check,login_url='/404')
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


@user_passes_test(check,login_url='/404')
def manage_user(request):
    if request.method == "POST":
        pass
    else:
        response = {'id':[],'name':[], 'position':[], 'phone_number':[],'position_all':[]}
        users = CustomUser.objects.all().filter(is_superuser = False)
        for user in users:
            response['id'].append(str(user.emp_id))
            response['name'].append(str(user.first_name +" "+ user.last_name))
            response['position'].append(str(user.position))
            response['phone_number'].append(str(user.phone_number))
        for pos in (StaffPosition.objects.all()):
            response['position_all'].append(str(pos))
        print(response)
        return render(request, 'AdminModule/manage_user.html',{'data':response})        


def user_profile(request,id):
    if request.method == "POST":
        pass
    else:
        try:
            user = CustomUser.objects.get(emp_id = str(id), is_superuser = False )
        except:
            return HttpResponseRedirect('/404')

        response = {'position_all':[]}
        response['id'] = user.id
        response['first_name'] = str(user.first_name)
        response['last_name'] = str(user.last_name)
        response['username'] = str(user.username)
        response['email'] = str(user.email)
        response['phone_number'] = str(user.phone_number)
        response['manager'] = str(user.is_rmanager)
        response['emp_id'] = str(user.emp_id)
        response['position'] = str(user.position)
        
        for pos in (StaffPosition.objects.all()):
                response['position_all'].append(str(pos))
        return render(request, 'AdminModule/edit_profile.html',{'data':response})

@user_passes_test(check, login_url="/404")
def admin_panel(request):
    return render(request, 'AdminModule/admin_panel.html')