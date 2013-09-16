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
        resource_name = 'core/event'
        authorization = DjangoAuthorization()
        filtering = {
            'category': ['exact'],
            'start_date': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'city' : ['exact']
        }
        paginator_class = Paginator
