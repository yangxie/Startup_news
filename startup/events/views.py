from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from core.models import Event
from core.common import *

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
          if (filter_option != ''):
               filter_options[filter_key] = filter_option
#     return filter_options
     return to_readable_options(filter_options)

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

def view_delete_event(request, event_id):
     try:
          event = Event.objects.get(pk=event_id)
          event.delete()
     except Event.DoesNotExist:
          pass
     return view_events(request)
