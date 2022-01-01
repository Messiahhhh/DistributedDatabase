from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from django import http
from django.shortcuts import render

# Create your views here.
from django.contrib import admin

from Database.settings import conns
from .models import ProductDetailInfo, OrderInfo, OrderDetailInfo, UserBasicInfo
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import datetime
import json
import pymongo
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


def dbtest(request):
    pass


def login(request):
    if request.method == 'POST':
        dict = json.loads(request.body)
        userName = dict["username"]
        passWord = dict["password"]
        # userName = request.POST.get("username")
        # passWord = request.POST.get("password")
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
            new_product = ProductDetailInfo(proName=name, descript=desc, price=price, image=img,
                                            reserveCount=reserveCount)
            new_product.save()
            return JsonResponse({"status": 0
                                 })
        else:
            if desc:
                tmp = ProductDetailInfo(proName=name).update(set__descript=str(desc))
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
        ProductDetailInfo(proName=_id).delete()
        return JsonResponse({"status": 0
                             })


def productList(request):
    if request.method == 'GET':
        products = ProductDetailInfo.objects.all().order_by("+proName")
        return JsonResponse({"status": 0,
                             "data": {
                                 "products": [
                                     {
                                         "imgs": i.image,
                                         "_id": i.id,
                                         "name": i.proName,
                                         "desc": i.descript,
                                         "price": i.price,
                                         "stock": i.reserveCount
                                     }
                                     for i in products
                                 ]
                             }
                             })


def orderCreate(request):

    orderDetail_col = conns["E_MARKET"]['order_detail_info']
    orderInfo_col = conns["E_MARKET"]['order_info']
    proDetail_col = conns["E_MARKET"]['product_detail_info']

    if request.method == 'POST':
        dict = json.loads(request.body)

        orderid = dict["_id"]  # 订单ID
        userid = dict["_userid"]
        totalPrice = dict["totalPrice"]
        products = dict["product"]

        with conns.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                # 创建订单详情
                OrderDetail = {
                    "_id": orderid,
                    "orderNo": None,
                    "userId": userid,
                    "sendName": None,
                    "sendAddress": None,
                    "sendZip": None,
                    "sendTel": None,
                    "payment": totalPrice,
                    "meno": None,
                    "time": datetime.datetime.now(),
                    "tag": None
                }

                # 生成物品清单 
                productList = []
                for thisOrder in products:
                    purchases = thisOrder["purchase"]
                    print("买了", purchases, "个", thisOrder['name'])

                    singleProduct = proDetail_col.find_one({'_id': thisOrder["name"]})
                    dict = {
                        "name": singleProduct['_id'],
                        "desc": singleProduct['descript'],
                        "price": singleProduct['price'],
                        "stock": singleProduct['reserveCount'] - purchases,
                        "img": singleProduct['image'],
                        "purchase": purchases
                    }
                    # 更新库存
                    proDetail_col.update(
                        {'_id': thisOrder["name"]},
                        {'$inc': {
                            'reserveCount': purchases * (-1)
                        }
                        }
                    )
                    # print("成功更新库存")
                    productList.append(dict)

                # 创建订单
                itemCount = len(productList)
                orderinfo = {
                    "orderId": orderid,
                    "count": itemCount,
                    "price": totalPrice,
                    "proId": productList
                }
                # print("成功创建一个orderinfo")

                try:
                    orderDetail_col.insert_one(document=OrderDetail)
                    # print("成功插入了一个OrderDetail")
                    orderInfo_col.insert_one(document=orderinfo)
                    # print("成功插入一个orderinfo")
                except:
                    # 操作异常，中断事务
                    session.abort_transaction()
                else:
                    session.commit_transaction()
                finally:
                    session.end_session()
        # with

        expiredTime = OrderDetail['time'] + datetime.timedelta(minutes=30) - datetime.datetime.now()
        expiredTime = expiredTime.total_seconds()
        return JsonResponse({
            "status": 0,
            "data": {
                "_id": orderid,
                "_userid": userid,
                "totalPrice": totalPrice,
                # 下单日期
                "create": OrderDetail['time'],
                # 过期时间 单位秒
                "expired": expiredTime,
                "products": productList
            }
        })
        # if


def orderList(request):
    if request.method == 'GET':

        orderDetail_col = conns['E_MARKET']['order_detail_info']
        orderInfo_col = conns['E_MARKET']['order_info']
        proDetail_col = conns['E_MARKET']['product_detail_info']

        with conns.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                # 生成订单列表
                orderList = []
                for thisOrder in orderDetail_col.find():
                    expiredTime = thisOrder['time'] + datetime.timedelta(seconds=30) - datetime.datetime.now()
                    expiredTime = expiredTime.total_seconds()

                    # 删除过期订单
                    if (expiredTime < 0):
                        findOrder = orderInfo_col.find_one({'orderId': thisOrder['_id']})
                        productList = findOrder['proId']
                        # print("成功找到该订单的商品列表")

                        # 恢复库存
                        count = 0
                        try:
                            for prod in productList:
                                count += 1
                                proDetail_col.update_one(
                                    {'_id': prod['name']},
                                    {'$inc': {
                                        'reserveCount': prod['purchase']
                                    }
                                    }
                                )
                                # print("恢复",prod['purchase'],"个",prod['name'])

                            # print("一共恢复了",count,"个商品库存")
                            # print("当前订单Id为：",thisOrder['_id'])
                            orderDetail_col.delete_one({'_id': thisOrder['_id']})
                            orderInfo_col.delete_one({'orderId': thisOrder['_id']})
                        except:
                            # 操作异常，中断事务
                            session.abort_transaction()
                        else:
                            session.commit_transaction()
                        finally:
                            session.end_session()
                        continue
                    # if

                    dict = {
                        "_id": thisOrder['_id'],
                        "_userid": thisOrder['userId'],
                        "totalPrice": thisOrder['payment'],
                        "create": thisOrder['time'],
                        "expired": expiredTime
                    }
                    orderList.append(dict)
                # for
    return JsonResponse({
        "status": 0,
        "data": {
            "orders": orderList
        }
    })
