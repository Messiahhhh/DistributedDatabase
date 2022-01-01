from celery import shared_task

from Database.settings import conns
from .models import ProductDetailInfo, OrderInfo, OrderDetailInfo, UserBasicInfo
import time
import pymongo
import datetime

@shared_task
def dynamicDelete():
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

