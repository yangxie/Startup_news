from django.db import models
from django.db.models import CharField, TextField, DateField, TimeField, SmallIntegerField

class News(models.Model):
    name = CharField(max_length=100)
    description = TextField(blank=True, null=True)
    category = CharField(max_length=50)
    date = DateField()
    start_time = TimeField()
    end_time = TimeField(blank=True, null=True)
    place = CharField(max_length=50)
    address_line1 = CharField(max_length=100)
    address_line2 = CharField(max_length=100, blank=True, null=True)
    city = CharField(max_length=100)
    state = CharField(max_length=100)
    postal_code = CharField(max_length=15)
    URL = CharField(max_length=200)
    coupon = CharField(max_length=50, blank=True, null=True)
    status = SmallIntegerField(default=1)
