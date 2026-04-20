# selenium_demo/urls.py 正确完整代码
from django.urls import path
from lists import views

urlpatterns = [
    path('', views.home_page, name='home'),
]