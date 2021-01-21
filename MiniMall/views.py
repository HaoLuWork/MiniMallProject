from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, path
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from MiniMall.models import GoodsInfo, User_Profile, OrderGoods
from MiniMall.forms import LoginForm, RegistrationForm




def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)
    input_info = LoginForm(request.POST)
    context['form'] = input_info

    if not input_info.is_valid():
        return render(request, 'login.html', context)

    new_user = authenticate(username=input_info.cleaned_data['username'],
                            password=input_info.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('home'))

def main_page_action(request):
    # return render(request,'home.html')
    # goods = GoodsInfo.objects.get.all()
    return render(request, 'home.html', {'goods' : GoodsInfo.objects.all()})

def item_details(request, id):
    item = GoodsInfo.objects.get(id = id)
    return render(request, 'item.html', {'item' : item})


def register_action(request):
    context = {}
    if request.method =='GET':
        context['form']=RegistrationForm()
        return render(request, 'Register.html', context)

    input_info = RegistrationForm(request.POST)
    context['form']=input_info

    if not input_info.is_valid():
        return render(request, 'Register.html', context)
    
    new_user = User.objects.create_user(username=input_info.cleaned_data['username'], 
                                        password=input_info.cleaned_data['password1'],
                                        email=input_info.cleaned_data['email'])
                                        # first_name=input_info.cleaned_data['first_name'],
                                        # last_name=input_info.cleaned_data['last_name']
    user = new_user.save()

    new_user = authenticate(username=input_info.cleaned_data['username'],
                            password=input_info.cleaned_data['password1'])

    login(request, new_user)
    create_profile(new_user)
    return redirect(reverse('home'))

@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('home'))




    # prev_url = request.META['HTTP_REFERER']
    # response = redirect(prev_url)
    # return response
    # 从哪儿来回哪儿去


@login_required
def add_cart(request, id):
    item = GoodsInfo.objects.get(id=id)
    # item = get_object_or_404(GoodsInfo, id=id)

    cur_order = OrderGoods(goods_info = item)
    # cur_order.save()
    # cur_order.goods_info = item
    # cur_order.goods_count = 1


    user = request.user

    User_Profile.objects.get(username = user).cart.add(cur_order)
    all_cart_item  = User_Profile.objects.get(username=user).cart.all()
    return render(request, 'cart.html', {'goods' : all_cart_item})


# def cart_del(request):

def open_cart(request):
    if request.method == 'GET':
        all_cart_item = User_Profile.objects.get(username=request.user).cart.all()
        return render(request, 'cart.html', {'goods' : all_cart_item})


def create_profile(user):
    new_profile = User_Profile(username = user)
    new_profile.save()


@login_required
def personal_info(request):
    context = {}
    if request.method == 'GET':
        user = request.user
        context = {'username': user.username, 'email' : user.email}
        return render(request, 'personalinfo.html', context)
    