from django.contrib import admin
from goods.models import *
from cart.models import *
# Register your models here.
admin.site.register(GoodsCategory)

admin.site.register(GoodsInfo)
admin.site.register(OrderGoods)
admin.site.register(OrderInfo)