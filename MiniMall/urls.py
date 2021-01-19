from django.urls import path
from MiniMall import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page_action, name='home'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)