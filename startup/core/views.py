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
from common.JsonResponse import JsonResponse

@ensure_csrf_cookie
def index_view(request):
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

from core.models import EventSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.views.generic import TemplateView

class EventsView(generics.ListCreateAPIView):
    model = Event
    serializer_class = EventSerializer

class EventView(generics.RetrieveUpdateDestroyAPIView):
    model = Event
    serializer_class = EventSerializer

#class HomeView(TemplateView):
#    template_name = 'home.html'

def get_templates_from_file(template_name):
    import os
    filepath = os.path.join(settings.STATIC_ROOT, "templates", template_name + ".html")
    filecontent = '<script type="text/x-handlebars" data-template-name="%s">' % template_name
    fin = open(filepath, "r")
    for line in fin:
        filecontent = filecontent + line + "\n"
    fin.close()
    filecontent = filecontent + "</script>"
    return filecontent

@ensure_csrf_cookie
def home_view(request):
    return render(request, 'home.html', {})
