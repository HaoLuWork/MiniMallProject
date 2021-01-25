from django.db import models

# Create your models here.
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


class OrderGoods(models.Model):
    # username = models.ForeignKey(User, on_delete=models.PROTECT)
    goods_info = models.ForeignKey('goods.GoodsInfo', on_delete=models.PROTECT)
    goods_num = models.IntegerField()
    goods_order = models.ForeignKey(OrderInfo, on_delete=models.PROTECT)

