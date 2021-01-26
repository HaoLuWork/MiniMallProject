from django.shortcuts import render, redirect
from django.http import HttpResponse
from goods.models import GoodsCategory, GoodsInfo
from cart.models import OrderInfo
from webapps.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, path

def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        context['user'] = ''
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
        context['user'] = ''
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

def logout_action(request):
    logout(request)
    return redirect(reverse('home'))

def personal_info(request):
    context = {}
    if request.method == 'GET':
        user = request.user
        cart_goods_list = []
        cart_goods_count = 0
        cart_goods_money = 0
        for goods_id, goods_num in request.COOKIES.items():
            if not goods_id.isdigit():
                continue
            cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
            cart_goods.goods_num = goods_num # 设置当前物品的数量
            cart_goods.goods_sum_price = cart_goods.goods_price * goods_num
                # cart_goods可以理解为单独的实例，而不是GoodsInfo类的实例
                # 所以可以给他创建额外的field，比如这里的goods_num
            cart_goods_list.append(cart_goods) # 把当前物品添加到list里
            cart_goods_count += int(goods_num) # 计算总数量
            cart_goods_money += int(cart_goods.goods_num) * int(cart_goods.goods_price) # 计算总价格
        context = {'username': user.username, 
                    'email' : user.email,
                    'cart_goods_list' : cart_goods_list,
                    'cart_goods_count' : cart_goods_count,
                    'cart_goods_money' : cart_goods_money}

        return render(request, 'personalinfo.html', context)
    


def index(request):
    # 查询商品的分类
    categories = GoodsCategory.objects.all()

    # 从每个分类中获取4个商品（每一类的最后4个（最新的））
    # for cag in categories:

    #     GoodsInfo.objects.filter(goods_cag = cag)
    #     # 一对多的关系，查询多的一方，可以用 少的一方_set.all()
    #     cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]
    # 获取当前用户
    if request.user.is_authenticated: 
        user = request.user
    else:
        user = ''

    # 获取全部商品列表
    goods_list = GoodsInfo.objects.all()
    # 获取购物车里所有的商品 用cookie
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
        cart_goods.goods_num = goods_num # 设置当前物品的数量
        cart_goods.goods_sum_price = cart_goods.goods_price * goods_num
            # cart_goods可以理解为单独的实例，而不是GoodsInfo类的实例
            # 所以可以给他创建额外的field，比如这里的goods_num
        cart_goods_list.append(cart_goods) # 把当前物品添加到list里
        cart_goods_count += int(goods_num) # 计算总数量
        cart_goods_money += int(goods_num) * cart_goods.goods_price


    # 购物车的商品总数量
    return render(request, 'home.html',{'categories' : categories,
                                        'user' : user,
                                        'cart_goods_list' : cart_goods_list, 
                                        'cart_goods_count' : cart_goods_count,
                                        'cart_goods_money' : cart_goods_money,
                                        'goods_list' : goods_list})


def item_details(request, id):
    if request.user.is_authenticated: 
        user = request.user
    else:
        user = ''
    item = GoodsInfo.objects.get(id = id)
    # goods_list = GoodsInfo.objects.all()
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
        cart_goods.goods_num = goods_num # 设置当前物品的数量
        cart_goods.goods_sum_price = cart_goods.goods_price * goods_num
            # cart_goods可以理解为单独的实例，而不是GoodsInfo类的实例
            # 所以可以给他创建额外的field，比如这里的goods_num
        cart_goods_list.append(cart_goods) # 把当前物品添加到list里
        cart_goods_count += int(goods_num) # 计算总数量
        cart_goods_money += int(cart_goods.goods_num) * int(cart_goods.goods_price) # 计算总价格
    return render(request, 'item.html', {'item' : item,
                                        'user' : user,
                                        'cart_goods_list' : cart_goods_list,
                                        'cart_goods_count' : cart_goods_count,
                                        'cart_goods_money' : cart_goods_money})


def show_cag(request, id):
    cag_id = str(id)
    item_list = GoodsInfo.objects.filter(goods_cag= cag_id)
    categories = GoodsCategory.objects.all()
    # 以下是购物车部分
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
        cart_goods.goods_num = goods_num # 设置当前物品的数量
        cart_goods.goods_sum_price = cart_goods.goods_price * goods_num
            # cart_goods可以理解为单独的实例，而不是GoodsInfo类的实例
            # 所以可以给他创建额外的field，比如这里的goods_num
        cart_goods_list.append(cart_goods) # 把当前物品添加到list里
        cart_goods_count += int(goods_num) # 计算总数量
        cart_goods_money += int(goods_num) * cart_goods.goods_price


    # 购物车的商品总数量
    return render(request, 'home.html',{'categories' : categories,
                                        'cart_goods_list' : cart_goods_list, 
                                        'cart_goods_count' : cart_goods_count,
                                        'cart_goods_money' : cart_goods_money,
                                        'goods_list' : item_list})

def order_finish(request):

    return render(request, 'placeOrder.html')

def submit_order(request):
    addr = request.POST.get('addr','')
    recv = request.POST.get('recv','')
    tele = request.POST.get('tele','')
    extra = request.POST.get('extra')

    order_info = OrderInfo()
    order_info.order_addr = addr
    order_info.order_tele = tele
    order_info.order_recv = recv
    order_info.order_extra = extra
    order_info.order_id = str(time.time() * 1000) + str(time.clock() * 1000000)
    order_info.save()