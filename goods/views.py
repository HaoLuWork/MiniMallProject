from django.shortcuts import render, redirect
from django.http import HttpResponse
from goods.models import GoodsCategory, GoodsInfo

# Create your views here.
def index(request):
    # 查询商品的分类
    categories = GoodsCategory.objects.all()

    # 从每个分类中获取4个商品（每一类的最后4个（最新的））
    # for cag in categories:

    #     GoodsInfo.objects.filter(goods_cag = cag)
    #     # 一对多的关系，查询多的一方，可以用 少的一方_set.all()
    #     cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]

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
                                        'cart_goods_list' : cart_goods_list, 
                                        'cart_goods_count' : cart_goods_count,
                                        'cart_goods_money' : cart_goods_money,
                                        'goods_list' : goods_list})


def item_details(request, id):
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
                                        'cart_goods_list' : cart_goods_list,
                                        'cart_goods_count' : cart_goods_count,
                                        'cart_goods_money' : cart_goods_money})


