from django.template import Context
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from core.models import Event


from django.shortcuts import render
from django.shortcuts import render_to_response
from core.models import Event
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings
import json
from common.JsonResponse import JsonResponse
from eventadmin.lib import crawlEventBrite

def view_add_event(request):
#    import json
#    response_data = {}
#    response_data['address'] = 'street'
#    response_data['category'] = 'restaurant'
    url = request.POST['event-url']
    response_data = crawlEventBrite(url)
    return JsonResponse([response_data.to_dict()])

def view_event_admin(request):
    c = Context()
    c['request'] = request
    sidebar = ''
    body = ''
    c['contents'] = render_to_string("events/event_admin.html", {'body': body, 'sidebar': sidebar}, context_instance=RequestContext(request))
    return render_to_response('common/base.html', c, context_instance=RequestContext(request))

