from django.urls import path
from MiniMall import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page_action, name='home'),
    # path('', views.register_action, name='home'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    #path('cart/<int:id>', views.add_cart, name='cart'),
    #path('item/<int:id>', views.item_details, name='details'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)