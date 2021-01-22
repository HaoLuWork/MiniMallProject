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
    # goods = GoodsInfo.objects.get.all()
    if request.user.is_authenticated: #如果有登陆
        # cart_goods_list = []
        # cart_goods_count = 0
        # 读取当前session里购物车相关的所有数据
        # for goods_id, goods_num in request.COOKIES.itmes()
        #     if not goods_id.isdigit():
        #         continue # 验证一下当前取出的key是否是数字，如果不是数字说明不是我们要的id
            
        #     cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
        #     cart_goods.goods_num = goods_num # 设置当前物品的数量
        #     cart_goods_list.append(cart_goods) # 把当前物品添加到list里
        #     cart_goods_count = cart_goods_count + int(goods_num) # list里物品的总数量要相应改变
        user = request.user
        all_cart_item  = User_Profile.objects.get(username=user).cart.all()
        User_Profile.objects.get(username = request.user).cart.all()
        return render(request, 'home.html', {'goods' : GoodsInfo.objects.all(), 'user' : request.user, 'cart_goods_list' : all_cart_item})
    return render(request, 'home.html', {'goods' : GoodsInfo.objects.all(), 'user' : ''})

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
def add_cart_from_home(request, id):
    item = GoodsInfo.objects.get(id=id)
    
    cart_list = User_Profile.objects.get(username = request.user).cart.all()
    # if cart_list.count() != 0:
    cur_order = OrderGoods.objects.get(goods_info = item, username = request.user)

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
    # return HttpResponseRedirect('home.html')

@login_required
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
    if request.method == 'GET':
        all_cart_item = User_Profile.objects.get(username=request.user).cart.all()
        return render(request, 'cart.html', {'cart_items' : all_cart_item})


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
    