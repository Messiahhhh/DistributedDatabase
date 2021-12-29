from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from django import http
from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from .models import ProductDetailInfo,OrderInfo,OrderDetailInfo,UserBasicInfo
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import datetime
import json

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
    if request.method == 'POST':
        dict = json.loads(request.body)

        orderid    = dict["_id"]        # 订单ID
        userid     = dict["_userid"]
        totalPrice = dict["totalPrice"]
        products   = dict["product"]

        userInfo = UserBasicInfo.objects(userName=userid)[0]

        # 创建订单详情
        OrderDetail=OrderDetailInfo(   orderId = orderid        ,
                                        userId = userInfo       , 
                                       payment = totalPrice     ).save()

        # 生成物品清单 
        productList = []
        for item in products:
            purchases  = item["purchase"]
            singleProduct = ProductDetailInfo.objects( proName = item["name"] )[0]
            dict = {
                 "name" : singleProduct.proName         ,
                 "desc" : singleProduct.descript        ,
                "price" : singleProduct.price           ,
                "stock" : singleProduct.reserveCount-purchases  ,
                  "img" : singleProduct.image           
            }
            # 更新库存
            singleProduct.update ( dec__reserveCount = purchases )
            productList.append(dict)

        # 创建订单
        itemCount = len(productList)
        OrderInfo( orderId = OrderDetail , 
                     count = itemCount   ,
                     price = totalPrice  ,
                     proId = productList ).save()
        
        expiredTime = OrderDetail.time + datetime.timedelta(days=1) - datetime.datetime.now()
        expiredTime = expiredTime.total_seconds()
        return JsonResponse ({   
                                "status": 0,
                                "data":{
                                           "_id" : orderid           ,
                                       "_userid" : userid            ,
                                    "totalPrice" : totalPrice        ,
                                        # 下单日期
                                        "create" : OrderDetail.time  ,
                                       # 还有1天过期 单位毫秒
                                       "expired" : expiredTime       ,    
                                      "products" : productList
                                }
                            })
        # if

def orderList(request):
    if request.method == 'GET':
        orders = OrderDetailInfo.objects()
        
        # 生成订单列表
        orderList = []
        for item in orders:
            expiredTime = item.time + datetime.timedelta(days=1) - datetime.datetime.now()
            expiredTime = expiredTime.total_seconds()
            dict = {
                       "_id" : item.orderId     ,
                   "_userid" : item.userId.id   ,
                "totalPrice" : item.payment     ,
                    "create" : item.time        ,
                   "expired" : expiredTime           
            }
            orderList.append(dict)

    return JsonResponse({
                            "status": 0,
                            "data": {
                                "orders":orderList
                            }
                        })