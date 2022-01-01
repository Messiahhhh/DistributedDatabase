from celery import shared_task
from .models import ProductDetailInfo, OrderInfo, OrderDetailInfo, UserBasicInfo
import time

@shared_task
def dynamicDelete():
    pass
