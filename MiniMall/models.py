from django.db import models

class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=100, verbose_name='商品名')
    goods_price = models.IntegerField(default=0, verbose_name='价格')
    goods_desc = models.CharField(max_length=2000, verbose_name='描述')
    goods_img = models.ImageField(upload_to='goods')
    # goods_cag modles.ForeignKey('goodsCategory')

    def __str__(self):
        return self.goods_name
    




