from django.urls import path
from MiniMall import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page_action, name='home'),
    path('login', views.login_action, name='login'),
    path('accounts/login/', views.login_action, name='login1'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('info', views.personal_info, name='info'),
    path('cart', views.open_cart, name='cart'),
    path('cart/<int:id>', views.add_cart, name='add_cart'),
    path('item/<int:id>', views.item_details, name='details'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)