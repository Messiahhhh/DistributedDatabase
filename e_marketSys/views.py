from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from .models import ProductDetailInfo, OrderInfo, OrderDetailInfo, UserBasicInfo
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
            return JsonResponse({"status": 1,
                                 "msg": "用户名或密码不正确！"
                                 })
        else:
            if check_password(passWord, checkUser[0].passWord):
                return JsonResponse({"status": 0,
                                     "data": {
                                         "_id": checkUser[0].id,
                                         "password": checkUser[0].passWord,
                                         "username": checkUser[0].userName,
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
    if request.method == 'POST':
        userName = request.POST.get("username")
        passWord = request.POST.get("password")
        checkUser = UserBasicInfo.objects(userName=userName)
        if checkUser:
            return JsonResponse({"status": 1,
                                 "msg": "此用户已存在"
                                 })
        else:
            encrypto = make_password(passWord)
            newUser = UserBasicInfo(userName=userName, passWord=encrypto)
            try:
                newUser.save()
                checkUser = UserBasicInfo.objects(userName=userName)
                return JsonResponse({"status": 0,
                                     "data": {
                                         "_id": checkUser[0].id,
                                         "username": checkUser[0].userName,
                                         "password": checkUser[0].passWord,
                                         "create_time": checkUser[0].registerTime,
                                     }
                                     })
            except Exception:
                return JsonResponse({"status": 1,
                                     "msg": "添加出错，请检查配置"
                                     })

    else:
        return HttpResponse(status=404)


def userUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        userName = request.POST.get("username")
        passWord = request.POST.get("password")
        checkUser = UserBasicInfo.objects(userName=userName)
        if checkUser:
            checkUser[0].id = id
            checkUser[0].userName = userName
            checkUser[0].passWord = make_password(passWord)
            try:
                checkUser[0].save()
                return JsonResponse({"status": 0,
                                     "data": {
                                         "_id": checkUser[0].id,
                                         "username": checkUser[0].userName,
                                         "password": checkUser[0].passWord,
                                     }
                                     }
                                    )
            except Exception:
                return JsonResponse({"status": 1,
                                     "msg": "更新出错，请咨询管理员"
                                     })
        else:
            return JsonResponse({"status": 1,
                                 "msg": "此用户不存在"
                                 })

    else:
        return HttpResponse(status=404)


def userList(request):
    pass


def userDelete(request):
    pass


def productAdd(request):
    pass

def productUpdate(request):
    if request.method == 'POST':
        _id = request.POST.get("_id")
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        img = request.POST.get("img")
        check = ProductDetailInfo(proName=name)
        if not check:
            new_product = ProductDetailInfo(proName=name, descript=desc, price=price, image=img)
            new_product.save()
            return JsonResponse({"status": 0
                                 })
        else:
            if not desc:
                tmp = ProductDetailInfo(proName = name).update(set_descript = desc)
            if not price:
                tmp = ProductDetailInfo(proName=name).update(set_price=desc)
            if not img:
                tmp = ProductDetailInfo(proName=name).update(set_image=img)
            return JsonResponse({"status": 0
                                 })


def productDelete(request):
    if request.method == 'POST':
        _id = request.POST.get("_id")
        ProductDetailInfo(proName= _id).delete()
        return JsonResponse({"status": 0
                                 })
def productList(request):
    if request.method == 'GET':
        products = ProductDetailInfo.objects.all().order_by("+proName")
        return  JsonResponse({"status":0,
                                 "data":{
                                     "products": [
                                         {
                                             "imgs":i.image,
                                             "_id" :i.id,
                                             "name":i.proName,
                                             "desc":i.descript,
                                             "price":i.price,
                                             "stock":i.reserveCount
                                         }
                                         for i in products
                                     ]
                                 }
                                 })
def orderCreate(request):
    pass


def orderList(request):
    pass
