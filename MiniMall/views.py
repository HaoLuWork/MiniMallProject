from django.shortcuts import render, get_object_or_404, redirect
from MiniMall.forms import *
from MiniMall.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)
    input_info = LoginForm(request.POST)

    new_user = authenticate(username=input_info.cleaned_data['username'],
                            password=input_info.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse(''))


def register_action(request):
    context = {}
    if request.method =='GET':
        context['form']=RegistrationForm()
        return render(request, '', context)

    empty_form = RegistrationForm(request.POST)
    context['form']=empty_form

    if not empty_form.is_valid():
        return render(request, '', context)
    
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    return redirect(reverse(''))





