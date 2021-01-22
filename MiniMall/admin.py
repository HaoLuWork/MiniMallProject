from django.contrib import admin
from MiniMall.models import GoodsInfo, OrderInfo, User_Profile, OrderGoods

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display=[  'id','goods_name', 'goods_price', 'goods_desc']
    # 每页显示数量
    list_per_page = 15
    # 上下控制栏是否显示
    # actions_on_top = True
    actions_on_bottom = True

    # 显示搜索框
    search_fields = ['id', 'goods_name']

admin.site.register(GoodsInfo, GoodsInfoAdmin)

class OrderInfoAdmin(admin.ModelAdmin):
    list_display=['id', 'order_id', 'order_recv', 'order_tele', 'order_extra', 'order_status']
    list_per_page = 15
    search_fields = ['id', 'order_id', 'order_recv', 'order_tele']

admin.site.register(OrderInfo, OrderInfoAdmin)
# 需要在models里导入一个model类
admin.site.register(User_Profile)

admin.site.register(OrderGoods)