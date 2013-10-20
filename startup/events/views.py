from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from core.models import Event

def get_parameter(request, key, default):
     try:
          return request.GET[key]
     except:
          return default

def all_filter_options():
    all_events = Event.objects.all()
    locations = {}
    categories = {}
    for event in all_events:
        locations[event.city] = 1
        categories[event.category] = 1
        
    options = {}
    options['city'] = locations.keys()
    options['category'] = categories.keys()
    return options

def show_events(request, events, page):
     c = Context()
     c['request'] = request
     sidebar = render_to_string("events/event_filter.html",
                                {'options': all_filter_options()},
                                context_instance=RequestContext(request))     

     filter_options = get_filter_options(request)
     header = render_to_string("events/event_header.html",
                               {'filter_options': filter_options},
                               context_instance=RequestContext(request))     

     EVENT_PER_PAGE = 10
     paginator = Paginator(events, EVENT_PER_PAGE)

     page = int(page)
     prev_page = page - 1
     next_page = page + 1
     if next_page > paginator.num_pages:
          next_page = -1
     if prev_page <= 0:
          prev_page = -1

     body = render_to_string("events/event_list.html",
                             {'events': paginator.page(page).object_list,
                              'pages': paginator.page_range,
                              'current_page': page,
                              'prev_page': prev_page,
                              'next_page': next_page
                              },
                              context_instance=RequestContext(request))
     c['contents'] = render_to_string("events/events.html",
                                      {'body': body,
                                       'sidebar': sidebar,
                                       'header': header},
                                      context_instance=RequestContext(request))
     return render_to_response('common/base.html', c,
                               context_instance=RequestContext(request))

def view_events(request):
     page = get_parameter(request, 'page', 1)
     events = Event.objects.all()
     return show_events(request, events, page)

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

def get_value_or_none(table, key):
     if (table.has_key(key)):
          return table[key]
     return None

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

def to_readable_options(filter_options):
     ret = {}
     for key, value in filter_options.items():
          ret[key] = unicode.replace(value, '_', ' ')
     return ret

def get_filter_options(request):
     filter_keys = ['category', 'city', 'date']
     filter_options = {}
     for filter_key in filter_keys:
          filter_option = request.session.get('filter_' + filter_key, '')
          filter_options[filter_key] = filter_option
     return to_readable_options(filter_options)
     
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

def view_delete_event(request, event_id):
     try:
          event = Event.objects.get(pk=event_id)
          event.delete()
     except Event.DoesNotExist:
          pass
     return view_events(request)
