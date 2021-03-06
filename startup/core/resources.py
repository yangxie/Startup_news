from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from core.models import Event


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'events'
        authorization = DjangoAuthorization()
        filtering = {
            'category': ['exact'],
            'start_date': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'city' : ['exact']
        }
        paginator_class = Paginator

        # This option is necessary cause ember-data expects
        # return data after a POST or PUT
        always_return_data = True
