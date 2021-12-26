from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from .models import ProductDetailInfo,OrderInfo,OrderDetailInfo,UserBasicInfo
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

def dbtest(request):
    pass
def login(request):
    if request.method == 'POST':
        userName = request.POST.get("username")
        passWord = request.POST.get("password")
        checkUser = UserBasicInfo.objects(userName=userName)
        if not checkUser:
            encrypto = make_password(passWord)
            newUser = UserBasicInfo(userName=userName,passWord=encrypto)
            newUser.save()
            checkUser = UserBasicInfo.objects(userName=userName)
            return JsonResponse({"status":0,
                                 "data":{
                                     "_id":checkUser.id,
                                     "password":passWord,
                                     "username":userName,
                                     "create_time":checkUser.registerTime
                                 }
                                 })
        else:
            if check_password(passWord,checkUser.passWord):
                return JsonResponse({"status": 0,
                                     "data": {
                                         "_id": checkUser.id,
                                         "password": passWord,
                                         "username": userName,
                                         "create_time": checkUser.registerTime
                                     }
                                     })
            else:
                return JsonResponse({"status": 1,
                                     "msg": "用户名或密码不正确！"
                                     })
    else:
        return HttpResponse(status=404)


def manageUserAdd(request):
    pass
def userUpdate(request):
    pass
def userList(request):
    pass
def userDelete(request):
    pass
def productAdd(request):
    pass
def productUpdate(request):
    pass
def productDelete(request):
    pass
def productList(request):
    pass
def orderCreate(request):
    pass
def orderList(request):
    pass