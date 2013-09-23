from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Event
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import json

class JsonResponse(HttpResponse):
    def __init__(self, content={}, mimetype=None, status=None, content_type=None):
        if not content_type:
            content_type = 'application/json'
        super(JsonResponse, self).__init__(json.dumps(content), mimetype=mimetype,
                                           status=status, content_type=content_type)

@ensure_csrf_cookie
def index_view(request):
#    import os
#    index_path = os.path.join(settings.STATIC_ROOT, 'app/core/base.html')
    return render(request, 'base.html')

def all_filter_options_view(request):
    all_events = Event.objects.all()
    locations = {}
    categories = {}
    for event in all_events:
        locations[event.city] = 1
        categories[event.category] = 1
        
    import json
    response_data = {}
    response_data['locations'] = locations.keys()
    response_data['categories'] = categories.keys()
    return JsonResponse(response_data)
