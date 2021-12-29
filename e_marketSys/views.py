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
        print("2")
        checkUser = UserBasicInfo.objects(userName=userName)
        print("1")
        if not checkUser:
            encrypto = make_password(passWord)
            newUser = UserBasicInfo(userName=userName,passWord=encrypto)
            print(newUser.userName)
            print("x")
            newUser.save()
            print("b")
            checkUser = UserBasicInfo.objects(userName=userName)
            print("a")
            return JsonResponse({"status":0,
                                 "data":{
                                     "_id":checkUser[0].id,
                                     "password":passWord,
                                     "username":userName,
                                     "create_time":checkUser[0].registerTime
                                 }
                                 })
        else:
            if check_password(passWord,checkUser[0].passWord):
                return JsonResponse({"status": 0,
                                     "data": {
                                         "_id": checkUser[0].id,
                                         "password": passWord,
                                         "username": userName,
                                         "create_time": checkUser[0].registerTime
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