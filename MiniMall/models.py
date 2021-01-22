from django.db import models
from django.contrib.auth.models import User

class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=100, verbose_name='商品名')
    goods_price = models.IntegerField(default=0, verbose_name='价格')
    # DecimaField(max_digits=None, decimal_places=None)
    # digits表示总位数，places表示小数位数
    goods_desc = models.CharField(max_length=2000, verbose_name='描述')
    goods_img = models.ImageField(upload_to='goods')
    # goods_cag modles.ForeignKey('goodsCategory')

    def __str__(self):
        return self.goods_name

class OrderGoods(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    goods_info = models.ForeignKey(GoodsInfo, on_delete=models.PROTECT)
    goods_num = models.IntegerField()
    # goods_order = models.ForeignKey(OrderInfo, on_delete=models.PROTECT)


class User_Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    # email = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='profile_photo')
    # regestion_data = models.DateTimeField()
    cart = models.ManyToManyField(OrderGoods, related_name= 'gouwuche')
    #预备一个清空购物车操作 my_object.relations.remove(*my_object.relations.all())



class OrderInfo(models.Model):
    order_id = models.CharField(max_length=100, verbose_name='订单编号') #订单编号
    order_addr = models.CharField(max_length=100) #收货地址
    order_recv = models.CharField(max_length=50, verbose_name='收件人') #收件人
    order_tele = models.CharField(max_length = 11, verbose_name='联系电话') #联系电话
    order_fee = models.IntegerField(default=10) #运费
    order_extra = models.CharField(max_length=200, verbose_name='备注') #备注
    status = (
        (1,'待付款'),
        (2,'待发货'),
        (3,'待收货'),
        (4,'已完成'),
    )
    order_status = models.IntegerField(default=1, choices=status, verbose_name='订单状态') #当前状态


