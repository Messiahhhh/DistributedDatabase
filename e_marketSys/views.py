from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from django import http
from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from .models import ProductDetailInfo, OrderInfo, OrderDetailInfo, UserBasicInfo
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import datetime
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



def dbtest(request):
    pass


def login(request):
    if request.method == 'POST':
        userName = request.POST.get("username")
        passWord = request.POST.get("password")
        checkUser = UserBasicInfo.objects(userName=userName)
        if not checkUser:
            encrypto = make_password(passWord)
            newUser = UserBasicInfo(userName=userName, passWord=encrypto)
            newUser.save()
            checkUser = UserBasicInfo.objects(userName=userName)
            return JsonResponse({"status": 0,
                                 "data": {
                                     "_id": checkUser[0].id,
                                     "password": passWord,
                                     "username": userName,
                                     "create_time": checkUser[0].registerTime
                                 }
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
        id = request.POST.get("_id")
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
      
# 查看所有用户
def userList(request):
    if request.method == 'GET':
        user_list = UserBasicInfo.objects()
        data = []
        for user in user_list:
            tmp = {}
            check_user = UserBasicInfo.objects(userName=user.userName)
            tmp['_id'] = check_user[0].id
            tmp['username'] = user.userName
            tmp['password'] = user.passWord
            tmp['create_time'] = user.registerTime
            data.append(tmp)
        return JsonResponse({
            "status": 0,
            "data": data,
        })

# 用户删除
def userDelete(request):
    if request.method == 'POST':
        dict = json.loads(request.body)
        user_name = dict['userId']
        delete_user = UserBasicInfo(userName=user_name)
        delete_user.delete()
        return JsonResponse({
            "status": 0,
        })


# 添加商品
def productAdd(request):
    if request.method == 'POST':
        dict = json.loads(request.body)
        proName = dict['name']
        descript = dict['desc']
        salePrice = dict['price']
        reserveCount = dict['stock']
        image = dict['img']

        # productImg = request.FILES['gxy']
        check_product = ProductDetailInfo.objects(proName=proName)

        # path = os.path.join(MEDIA_ROOT, 'product')
        # path = os.path.join(path, productImgName)
        # uploaded_file = request.FILES['']
        # file = open(path, 'wb+')
        # for chunk in uploaded_file.chunks():
        #     file.write(chunk)
        # file.close()
        newProduct = ProductDetailInfo(proName=proName, descript=descript, salePrice=salePrice,
                                       reserveCount=reserveCount, image=image)
        newProduct.save()

        if not check_product:
            return JsonResponse({
                "status": 0,
                "data": {
                    "_id": check_product[0].id,
                    "name": proName,
                    "desc": descript,
                    "price": salePrice,
                    "stock": reserveCount,
                    "img": image,
                }
            })
        else:
            return JsonResponse({
                "status": 1,
                "msg": "商品已存在！",
            })

def productUpdate(request):
    if request.method == 'POST':
        _id = request.POST.get("_id")
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        img = request.POST.get("img")
        reserveCount = request.POST.get("reserveCount")
        check = ProductDetailInfo.objects(proName=name)
        if not check:
            new_product = ProductDetailInfo(proName=name, descript=desc, price=price, image=img,reserveCount=reserveCount)
            new_product.save()
            return JsonResponse({"status": 0
                                 })
        else:
            if desc:
                tmp = ProductDetailInfo(proName = name).update(set__descript = str(desc))
            if price:
                tmp = ProductDetailInfo(proName=name).update(set__price=price)
            if img:
                tmp = ProductDetailInfo(proName=name).update(set__image=str(img))
            if reserveCount:
                tmp = ProductDetailInfo(proName=name).update(set__reserveCount=reserveCount)
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
    if request.method == 'POST':
        dict = json.loads(request.body)

        orderid = dict["_id"]  # 订单ID
        userid = dict["_userid"]
        totalPrice = dict["totalPrice"]
        products = dict["product"]

        userInfo = UserBasicInfo.objects(userName=userid)[0]


        # 创建订单详情
        OrderDetail = OrderDetailInfo(orderId=orderid,
                                      userId=userInfo,
                                      payment=totalPrice).save()


        # 生成物品清单 
        productList = []
        for item in products:
            print(item)
            purchases = item["purchase"]
            singleProduct = ProductDetailInfo.objects(proName=item["name"])[0]
            dict = {
                "name": singleProduct.proName,
                "desc": singleProduct.descript,
                "price": singleProduct.price,
                "stock": singleProduct.reserveCount - purchases,
                "img": singleProduct.image
            }
            # 更新库存
            singleProduct.update(dec__reserveCount=purchases)
            productList.append(dict)

        # 创建订单
        itemCount = len(productList)
        OrderInfo(orderId=OrderDetail,
                  count=itemCount,
                  price=totalPrice,
                  proId=productList).save()

        expiredTime = OrderDetail.time + datetime.timedelta(days=1) - datetime.datetime.now()
        expiredTime = expiredTime.total_seconds()
        return JsonResponse({
            "status": 0,
            "data": {
                "_id": orderid,
                "_userid": userid,
                "totalPrice": totalPrice,
                # 下单日期
                "create": OrderDetail.time,
                # 还有1天过期 单位毫秒
                "expired": expiredTime,
                "products": productList
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
                "_id": item.orderId,
                "_userid": item.userId.id,
                "totalPrice": item.payment,
                "create": item.time,
                "expired": expiredTime
            }
            orderList.append(dict)

    return JsonResponse({
        "status": 0,
        "data": {
            "orders": orderList
        }
    })
