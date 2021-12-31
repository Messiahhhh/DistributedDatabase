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
import pymongo


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

bindip = "192.168.43.195"

def orderCreate(request):
    conns = pymongo.MongoClient(bindip, 27017)
    
    orderDetail_col = conns["E_MARKET"]['order_detail_info']
    orderInfo_col   = conns["E_MARKET"]['order_info']
    proDetail_col   = conns["E_MARKET"]['product_detail_info']

    if request.method == 'POST':
        dict = json.loads(request.body)

        orderid    = dict["_id"]        # 订单ID
        userid     = dict["_userid"]
        totalPrice = dict["totalPrice"]
        products   = dict["product"]

        with conns.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                # 创建订单详情
                OrderDetail = {
                            "_id" : orderid                 ,
                        "orderNo" : None                    ,
                         "userId" : userid                  ,
                       "sendName" : None                    ,
                    "sendAddress" : None                    ,
                        "sendZip" : None                    ,
                        "sendTel" : None                    ,
                        "payment" : totalPrice              ,
                           "meno" : None                    ,
                           "time" : datetime.datetime.now() ,
                            "tag" : None
                }
                

                # 生成物品清单 
                productList = []
                for thisOrder in products:
                    purchases  = thisOrder["purchase"]
                    print("买了",purchases,"个",thisOrder['name'])
                    
                    singleProduct = proDetail_col.find_one({'_id':thisOrder["name"]})
                    dict = {
                        "name" : singleProduct['_id']                      ,
                        "desc" : singleProduct['descript']                 ,
                        "price" : singleProduct['price']                    ,
                        "stock" : singleProduct['reserveCount']-purchases   ,
                        "img" : singleProduct['image']                    ,
                    "purchase" : purchases
                    }
                    # 更新库存
                    proDetail_col.update(
                        { '_id' : thisOrder["name"]},
                        { '$inc': {
                                'reserveCount':purchases*(-1)
                            }
                        }
                    )
                    # print("成功更新库存")
                    productList.append(dict)

                # 创建订单
                itemCount = len(productList)
                orderinfo = {
                    "orderId" : orderid     ,
                    "count" : itemCount   ,
                    "price" : totalPrice  ,
                    "proId" : productList
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
        return JsonResponse ({   
                                "status": 0,
                                "data":{
                                           "_id" : orderid           ,
                                       "_userid" : userid            ,
                                    "totalPrice" : totalPrice        ,
                                        # 下单日期
                                        "create" : OrderDetail['time']  ,
                                       # 过期时间 单位秒
                                       "expired" : expiredTime       ,    
                                      "products" : productList
                                }
                            })
        # if


def orderList(request):
    if request.method == 'GET':
        conns = pymongo.MongoClient(bindip, 27017)

        orderDetail_col = conns['E_MARKET']['order_detail_info']
        orderInfo_col   = conns['E_MARKET']['order_info']
        proDetail_col   = conns['E_MARKET']['product_detail_info']

        with conns.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                # 生成订单列表
                orderList = []
                for thisOrder in orderDetail_col.find():
                    expiredTime = thisOrder['time'] + datetime.timedelta(seconds=30) - datetime.datetime.now()
                    expiredTime = expiredTime.total_seconds()

                    # 删除过期订单
                    if (expiredTime < 0):
                        findOrder = orderInfo_col.find_one({'orderId':thisOrder['_id']})
                        productList = findOrder['proId']
                        # print("成功找到该订单的商品列表")

                        # 恢复库存
                        count = 0
                        try:
                            for prod in productList:
                                count += 1
                                proDetail_col.update_one(
                                    { '_id':prod['name'] },
                                    { '$inc':
                                        {
                                            'reserveCount':prod['purchase']
                                        }
                                    }
                                )
                                # print("恢复",prod['purchase'],"个",prod['name'])

                            # print("一共恢复了",count,"个商品库存")
                            # print("当前订单Id为：",thisOrder['_id'])
                            orderDetail_col.delete_one({'_id':thisOrder['_id']})
                            orderInfo_col.delete_one({'orderId':thisOrder['_id']})
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
                            "_id" : thisOrder['_id']     ,
                        "_userid" : thisOrder['userId']      ,
                        "totalPrice" : thisOrder['payment']     ,
                            "create" : thisOrder['time']        ,
                        "expired" : expiredTime           
                    }
                    orderList.append(dict)
                # for
    return JsonResponse({
                            "status": 0,
                            "data": {
                                "orders":orderList
                            }
                        })