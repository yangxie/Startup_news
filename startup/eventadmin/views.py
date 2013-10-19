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

from django import forms

class EventEditForm(forms.Form):
    GENERAL = 'GE'
    CONFERENCE = 'CO'
    CATEGORY_CHOICES = (
        (GENERAL, 'General'),
        (CONFERENCE, 'Conference'),
    )
    category = forms.ChoiceField(
        label='Category',
        choices=CATEGORY_CHOICES, initial=CONFERENCE,
        widget=forms.Select(attrs={'class': 'selectpicker form-control', 'placeholder': 'Category'}),
        error_messages={'required': 'Please select a category'}
        )

    name = forms.CharField(
         max_length=100, 
         label='Name',
         widget=forms.TextInput(
              attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
         error_messages={'required': 'Please enter the name', 'max_length': 'Maximum 100 characters'})
    
    address_line1 = forms.CharField(
         label='AddressLine1',
         widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "Address Line 1"}),
         error_messages={'required': 'Please enter the address'})

    address_line2 = forms.CharField(
         label='AddressLine2',
         widget=forms.TextInput(
              attrs={'class': 'form-control', 'placeholder': "Address Line 2"}),
         error_messages={})

    city = forms.CharField(
         label='City',
         widget=forms.TextInput(
              attrs={'class': 'form-control', 'placeholder': "City"}),
         error_messages={'required': 'Please enter the city'})

    state = forms.CharField(
         label='State',
         widget=forms.TextInput(
              attrs={'class': 'form-control', 'placeholder': "State"}),
         error_messages={'required': 'Please enter the state'})

    postal_code = forms.CharField(
         label='Postal code',
         widget=forms.TextInput(
              attrs={'class': 'form-control', 'placeholder': "Postal code"}),
         error_messages={'required': 'Please enter the postal code'})

    URL = forms.CharField(
         label='Url',
         widget=forms.TextInput(
              attrs={'class': 'form-control', 'placeholder': "Url"}),
         error_messages={'required': 'Please enter the postal url'})

    start_date = forms.DateField(
         label='Start Date', help_text='',
         widget=forms.DateInput(attrs={'class': 'form-control'}),
         error_messages={'required': 'Please choose the start date', 'invalid': 'Please choose a valid date'})

    end_date = forms.DateTimeField(
         label='End Date', help_text='',
         widget=forms.DateInput(attrs={'class': 'form-control'}),
         error_messages={'required': 'Please choose the end date', 'invalid': 'Please choose a valid date'})

def view_add_event(request):
#    import json
#    response_data = {}
#    response_data['address'] = 'street'
#    response_data['category'] = 'restaurant'
    url = request.POST['event-url']
    response_data = crawlEventBrite(url)
#    return JsonResponse([response_data.to_dict()])
    c = Context()
    c['request'] = request
    c['contents'] = render_to_string(
        "events/event_edit.html",
        {'form': EventEditForm(response_data.to_dict())}, context_instance=RequestContext(request))
    return render_to_response('common/base.html', c, context_instance=RequestContext(request))

def view_edit_event(request):
    operation = {'success': True, 'msg': ''}
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if (form.is_valid()):
            event = Event.objects.filter(name=form.cleaned_data['name'])
            if not event.exists():
                event = event[0]
            
                for attr, value in form.cleaned_data.iteritems(): 
                    setattr(event, attr, value)
                try:
                    event.save()
                    operation['success'] = True
                    operation['msg'] = 'Successfully updated the event.'
                except:
                    operation['success'] = False
                    operation['msg'] = 'Unkown errors '
            
    c = Context()
    c['request'] = request
    c['contents'] = render_to_string(
        "events/event_edit.html",
        {'form': form, 'form_msg': operation['msg']},
        context_instance=RequestContext(request))
    return render_to_response('common/base.html', c, context_instance=RequestContext(request))
            

def view_event_admin(request):
    c = Context()
    c['request'] = request
    sidebar = ''
    body = ''
    c['contents'] = render_to_string("events/event_admin.html", {'body': body, 'sidebar': sidebar}, context_instance=RequestContext(request))
    return render_to_response('common/base.html', c, context_instance=RequestContext(request))

