from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from core.models import News


class NewsResource(ModelResource):
    class Meta:
        queryset = News.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'core/news'
        authorization = DjangoAuthorization()
        filtering = {
            'category': ALL,
            'date': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
