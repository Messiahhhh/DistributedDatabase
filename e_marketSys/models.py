from django.db import models

# Create your models here.

import mongoengine
import datetime

class ProductDetailInfo(mongoengine.Document):
    proName = mongoengine.StringField(primary_key=True)
    saleCount = mongoengine.IntField(null=True)
    image = mongoengine.StringField(null=True)
    price = mongoengine.FloatField(null=True)
    salePrice = mongoengine.FloatField(null=True)
    descript = mongoengine.StringField(null=True)
    saleDate = mongoengine.DateTimeField(null=True)
    reserveCount = mongoengine.IntField(null=True)


class OrderInfo(mongoengine.Document):
    orderId = mongoengine.ReferenceField('OrderDetailInfo')
    count = mongoengine.IntField(null=True)
    price = mongoengine.FloatField(null=True)
    proId = mongoengine.ListField(mongoengine.ReferenceField('ProductDetailInfo'))


class OrderDetailInfo(mongoengine.Document):
    orderId = mongoengine.StringField(primary_key=True)
    orderNo = mongoengine.IntField(null=True)
    userId = mongoengine.ReferenceField('UserBasicInfo')
    sendName = mongoengine.StringField(null=True)
    sendAddress = mongoengine.StringField(null=True)
    sendZip = mongoengine.StringField(null=True)
    sendTel = mongoengine.StringField(null=True)
    payment = mongoengine.FloatField(null=True)
    meno = mongoengine.StringField(null=True)
    time = mongoengine.DateTimeField(default=datetime.datetime.now)
    tag = mongoengine.IntField(null=True)

    
class UserBasicInfo(mongoengine.Document):
    userName = mongoengine.StringField(primary_key=True)
    passWord = mongoengine.StringField(null=True)
    realName = mongoengine.StringField(null=True)
    tel = mongoengine.StringField(null=True)
    address = mongoengine.StringField(null=True)
    zip = mongoengine.StringField(null=True)
    email = mongoengine.StringField(null=True)
    registerTime = mongoengine.DateTimeField(default=datetime.datetime.now)

