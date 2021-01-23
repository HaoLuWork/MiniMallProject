from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
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
    # 需要返回的内容： 
    #   一个商品列表 ： GoodsInfo.objects.all()
    #   一个用户信息 ： request.user
    #   一个购物车列表：
        #   如果登陆，从数据库读取
        #   如果没登陆，从cookies读取
    #   一个购物车内商品总数（用于下拉菜单显示）
    
    all_goods = GoodsInfo.objects.all()
    user = ''
    #   如果已经登陆， 则刷新的时候从数据库读取购物车内容
    if request.user.is_authenticated: 
        cart_goods_count = 0
        user = request.user
        all_cart_item  = User_Profile.objects.get(username=user).cart.all()
        for item in all_cart_item:
            cart_goods_count += item.goods_num
        return render(request, 'home.html', {'goods' : all_goods, 'user' : user, 'cart_goods_list' : all_cart_item, 'cart_goods_count' : cart_goods_count})
        # all_cart_item  = User_Profile.objects.get(username=user).cart.all()
        # return render(request, 'home.html', {'goods' : GoodsInfo.objects.all(), 'user' : request.user, 'cart_goods_list' : all_cart_item})
    # 如果还未登陆，则刷新的时候从cookie读取购物车内容
    else:
        cart_goods_list = []
        cart_goods_count = 0
        for goods_id, goods_num in request.COOKIES.items():
            if not goods_id.isdigit():
                continue # 
            cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
            cart_goods.goods_num = goods_num # 设置当前物品的数量
            cart_goods_list.append(cart_goods) # 把当前物品添加到list里
            cart_goods_count += int(goods_num) # 计算总数量
        return render(request, 'home.html', {'goods' : all_goods, 'user' : user, 'cart_goods_list' : cart_goods_list, 'cart_goods_count' : cart_goods_count})
    # return render(request, 'home.html', {'goods' : goods, 'user' : ''})

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




def add_cart_from_home(request, id):
    # 如果想要避免对不存在的object做get，可以考虑先把当前东西存进cookie，再从cookie读取到数据库吗？？？
    # 如果已经登陆，则把数据添加到数据库中
    if request.user.is_authenticated: 
        # 拿到商品，拿到数量
        # 商品是GoodsInfo类，
        # 要存入购物车的是 OrderGoods类
        item = GoodsInfo.objects.get(id=id)
        
        cart_list = User_Profile.objects.get(username = request.user).cart.all()
        # if cart_list.count() != 0:
        # cur_order = OrderGoods.objects.get(goods_info = item, username = request.user)

            # 如果已经有了，则数量加1,
        if cur_order in cart_list:
            cur_item = OrderGoods.objects.get(goods_info = item)
            cur_item.goods_num = cur_item.goods_num + 1
        # 如果还没有，则直接添加
        else:
            cur_item = OrderGoods.objects.create(username = request.user, goods_info = item, goods_num =1)
            User_Profile.objects.get(username = request.user).cart.add(cur_item)
        # all_cart_item  = User_Profile.objects.get(username=user).cart.all()
        # return render(request, 'home.html', {'cart_item' : all_cart_item})
        return redirect(reverse('home'))
        # 如果没有登陆，则把数据添加到cookie中
    else:
        goods_id = str(id)
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id)
        if goods_count:
            goods_count = int(goods_count)+1
        else:
            goods_count=1
        response.set_cookie(goods_id, goods_count)
        return response




    # return HttpResponseRedirect('home.html')

    # 如果已经登陆，则写入cookie的同时也要写入数据库
    # 如果还未登陆，则只写入cookies

def add_cart_from_item(request, id):
    item = GoodsInfo.objects.get(id=id)
    cur_order = OrderGoods.objects.create(goods_info = item, goods_num =1)

    user = request.user

    User_Profile.objects.get(username = user).cart.add(cur_order)
    # all_cart_item  = User_Profile.objects.get(username=user).cart.all()
    # return render(request, 'home.html', {'goods' : all_cart_item})
    # return redirect('item/id.html')
    # return HttpResponseRedirect("")
    return redirect(reverse("{% url 'details' item.id %}"))

# def cart_del(request):


def open_cart(request):
    # 需要返回：
    #   每个商品的：名称，价格，数量，总价格
    #   所有商品的：总价格

    # 如果登陆了，则从数据库当中读取出相应的数据
    # cart_goods_list是OrderGoods 类，内含 goods_info(外键的GoodsInfo类), goods_num
    if request.user.is_authenticated: 
        sum_count = 0
        sum_price = 0
        cart_goods_list = User_Profile.objects.get(username=request.user).cart.all()
        for item in cart_goods_list:
            sum_count += item.goods_num
            sum_price += item.goods_info.goods_price * item.goods_num
        return render(request, 'cart.html', {'cart_goods_list' : cart_goods_list,
                                            'cart_goods_count' : sum_count,
                                            'cart_goods_money' : sum_price})
    # 如果还未登陆，则从cookies里读取内容
    # add_cart方法会将暂存如购物车的内容存如cookies，只需要读取出来返回即可
    else:
        cart_goods_list = []
        cart_goods_count = 0
        cart_goods_money = 0
        for goods_id, goods_num in request.COOKIES.items():
            if not goods_id.isdigit():
                continue
            cart_goods = GoodsInfo.objects.get(id = goods_id)
            cart_goods.goods_num = goods_num
            cart_goods.total_money = int(goods_num) * cart_goods.goods_price
            cart_goods_list.append(cart_goods)
            cart_goods_count += int(goods_num)
            cart_goods_money += int(goods_num)* cart_goods.goods_price
        return render(request, 'cart.html', {'cart_goods_list' : cart_goods_list,
                                            'cart_goods_count' : cart_goods_count,
                                            'cart_goods_money' : cart_goods_money})


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
    