from django.db import models
from django.db.models import CharField, TextField, DateField, TimeField, SmallIntegerField
from django.forms.models import model_to_dict
from rest_framework import serializers


class Event(models.Model):
    GENERAL = 'GE'
    CONFERENCE = 'CO'
    VENTURE = 'VE'
    CATEGORY_CHOICES = (
        (GENERAL, 'General'),
        (CONFERENCE, 'Conference'),
        (VENTURE, 'Venture Capital'),
        )

    name = CharField(max_length=100)
    description = TextField(blank=True, null=True)
    category = CharField(max_length=50)
    start_date = DateField()
    end_date = DateField()
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
    
    def __unicode__(self):
        return self.name

    def to_dict(self):
        return model_to_dict(self, fields=[], exclude=[])
    
    def category_full(self):
        for choices in Event.CATEGORY_CHOICES:
            if (choices[0] == self.category):
                return choices[1]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'category', 'start_date', 'end_date',
                  'start_time', 'end_time', 'place', 'address_line1',
                  'address_line2', 'city', 'state', 'postal_code', 'URL',
                  'coupon', 'status')
