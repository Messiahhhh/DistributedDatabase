from django.db import models

# Create your models here.

import mongoengine

class StudentModel(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    age = mongoengine.IntField()
    password = mongoengine.StringField(max_length=32)

