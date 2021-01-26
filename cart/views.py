from django.shortcuts import render, redirect
from goods.models import GoodsCategory, GoodsInfo

def add_cart(request, id, count):
    # 获取传进来的商品id
    # 把商品id存入cookie
    # 如果之前就已经存在了，那就把数量+1
        # 如果可以在url里把地址写成cart/<int:id>/<int:count>的话，没准可以调两个参数
    # 如果没有，那就添加一个新的
    goods_id = str(id)
    prev_url = request.META['HTTP_REFERER']
    response = redirect(prev_url)
    goods_count = request.COOKIES.get(goods_id)
    if goods_count:
        if not int(goods_count) > 99-count:
            goods_count = int(goods_count)+count
    else:
        goods_count= count
    response.set_cookie(goods_id, goods_count)
    return response

def open_cart(request):
    if request.user.is_authenticated: 
        user = request.user
    else:
        user = ''
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue # 
        cart_goods = GoodsInfo.objects.get(id=goods_id) # 找到当前id对应的物品
        cart_goods.goods_num = goods_num # 设置当前物品的数量
        cart_goods.sum_price = int(goods_num) * int(cart_goods.goods_price)
        cart_goods_list.append(cart_goods) # 把当前物品添加到list里
        cart_goods_count += int(goods_num) # 计算总数量
        cart_goods_money += int(goods_num) * cart_goods.goods_price
    cart_goods_list.sort(key = lambda x:x.id)
    return render(request, 'cart.html', {'cart_goods_list' : cart_goods_list, 
                                            'cart_goods_count' : cart_goods_count , 
                                            'cart_goods_money' : cart_goods_money,
                                            'user' : user,})

def remove_cart(request, id):
    goods_id = str(id)
    prev_url = request.META['HTTP_REFERER']
    response = redirect(prev_url)
    goods_count = request.COOKIES.get(goods_id)
    if goods_count:
        response.delete_cookie(goods_id)
    return response

def cart_item_pp(request, id):
    goods_id = str(id)
    prev_url = request.META['HTTP_REFERER']
    response = redirect(prev_url)
    goods_count = request.COOKIES.get(goods_id)
    if not int(goods_count) >= 99 :
        goods_count = int(goods_count) + 1
    response.set_cookie(goods_id, goods_count)
    return response

def cart_item_mm(request, id):
    goods_id = str(id)
    prev_url = request.META['HTTP_REFERER']
    response = redirect(prev_url)
    goods_count = request.COOKIES.get(goods_id)
    if not int(goods_count) <= 1 :
        goods_count = int(goods_count) - 1
    response.set_cookie(goods_id, goods_count)
    return response

# def place_order(request):
