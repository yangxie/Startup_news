from django.shortcuts import render
from django.shortcuts import render_to_response
from core.models import Event
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings
import json
from common.JsonResponse import JsonResponse

def event_url_process_view(request):
    import json
    response_data = {}
    response_data['address'] = 'street'
    response_data['category'] = 'restaurant'
    return JsonResponse(response_data)
