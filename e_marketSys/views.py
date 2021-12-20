from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from .models import StudentModel
from django.http import HttpResponse

def post(request):
    name = "nihao"
    age = 18
    password = "123456"
    stu = StudentModel(name=name,age=age,password=password)
    stu.save()
    cate = StudentModel.objects.all()
    print(cate)
    return HttpResponse(content="fuck")