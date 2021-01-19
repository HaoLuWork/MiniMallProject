from django.urls import path
from MiniMall import views
urlpatterns = [
    path('', views.main_page_action, name='home'),
]