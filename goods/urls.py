from django.urls import path
from goods import views
from cart.views import add_cart, open_cart, remove_cart, cart_item_pp, cart_item_mm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    # path('', views.main_page_action, name='home'),
    path('login', views.login_action, name='login'),
    # path('accounts/login/', views.login_action, name='login1'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('info', views.personal_info, name='info'),
    path('cart', open_cart, name='cart'),
    path('cart/<int:id>/<int:count>', add_cart, name='add_cart'),
    path('cart_item_pp/<int:id>', cart_item_pp, name='cart_item_pp'),
    path('cart_item_mm/<int:id>', cart_item_mm, name='cart_item_mm'),
    # path('cart2/<int:id>', views.add_cart_from_item, name='add_cart_from_item'),
    path('remove_cart/<int:id>', remove_cart, name='remove_cart'),
    path('item/<int:id>', views.item_details, name='details'),
    path('cag/<int:id>', views.show_cag, name='cag'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)