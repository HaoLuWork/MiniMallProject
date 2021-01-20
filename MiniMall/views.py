from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, path
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from MiniMall.models import GoodsInfo
from MiniMall.forms import LoginForm, RegistrationForm

def main_page_action(request):
    # return render(request,'home.html')
    # goods = GoodsInfo.objects.get.all()
    return render(request, 'home.html', {'goods' : GoodsInfo.objects.all()})

def item_details(request, id):
    item = GoodsInfo.objects.get(id = id)
    return render(request, 'item.html', {'item' : item})



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
    new_cart = OrderInfo()
    new_cart.save()
    return redirect(reverse('home'))

@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('home'))

@login_required
def add_cart(request, id):
    goods_id = request.GET.get('id','')
    # if goods_id:
    prev_url = request.META['HTTP_REFERER']
    # response = redirect("{% url 'details' id %}")
    response = redirect(prev_url)
    goods_count = request.COOKIES.get(id)
    if goods_count:
        goods_count = int(goods_count)+1
    else:
        goods_count = 1
    response.set_cookie(id, goods_count)
    return response
    # order = OrderInfo.objects.create(order_id=order_id,
    #                                 user=user,
    #                                 addr=addr_obj,
    #                                 pay_method=pay_id,
    #                                 transit_price=transport_price,
    #                                 product_count=total_count,
    #                                 product_price=total_price)
