"""Database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from e_marketSys import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login),
    path('manage/user/add', views.manageUserAdd),
    path('manage/user/update', views.userUpdate),
    path('manage/user/list', views.userList),
    path('manage/user/delete', views.userDelete),
    path('manage/product/add', views.productAdd),
    path('manage/product/update', views.productUpdate),
    path('manage/product/delete', views.productDelete),
    path('manage/product/list', views.productList),
    path('manage/order/create', views.orderCreate),
    path('manage/order/list', views.orderList),
    path('dbtest', views.dbtest)


]
