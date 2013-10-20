from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from core.models import Event
from core.common import *
from events.views import show_events


def filter_event_by_date(shift_days, window_range, kwargs):
     FOREVER = -1
     import datetime
     date = datetime.date.today()
     start_week = date - datetime.timedelta(date.weekday())
     start_day = start_week + datetime.timedelta(shift_days)
     end_day = start_week + datetime.timedelta(shift_days + window_range)

     if (window_range != FOREVER):
          kwargs['start_date__range'] = [start_day, end_day]
     else:
          kwargs['start_date__gt'] = start_day
     return kwargs

def date_filter_map(key):
     table = {}
     table['today'] = [0, 1]
     table['week'] = [0, 7]
     table['next_week'] = [7, 7]
     table['no_filter'] = [0, -1]
     return get_value_or_none(table, key)

def add_filter_by_option(filter_args, field, value):
     if (value != 'no_filter'):
          filter_args[field + '__exact'] = value
     return filter_args

def set_filter_option(request):
     filter_keys = ['category', 'city', 'date']
     for filter_key in filter_keys:
          filter_option = get_parameter(request, filter_key, '')
          if (filter_option != ''):
               request.session['filter_' + filter_key] = filter_option

     
def get_filter_kwargs(request):
     filter_keys = ['category', 'city', 'date']
     filter_kwargs = {}
     for filter_key in filter_keys:
          filter_option = request.session.get('filter_' + filter_key, '')
          if (filter_option != ''):
               if (filter_key == 'date'):
                    add_days = date_filter_map(filter_option)
                    filter_kwargs = filter_event_by_date(add_days[0], add_days[1], filter_kwargs)
               else:
                    filter_kwargs = add_filter_by_option(filter_kwargs, filter_key, filter_option)
     return filter_kwargs

def view_events_filter(request):
     events = []
     date_filter_option = get_parameter(request, 'date', '')

     filter_keys = ['category', 'city']
     set_filter_option(request)
     filter_kwargs = get_filter_kwargs(request)
     print filter_kwargs
     events = Event.objects.filter(**filter_kwargs)

     return show_events(request, events, 1)
